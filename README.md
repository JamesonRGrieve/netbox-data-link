<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
# netbox-data-link

A NetBox 4.6 plugin: a **native source of truth for a switch's data-link (OSI layer-2)
control-plane features** — Spanning Tree (STP/RSTP/MSTP), LLDP, and DHCP snooping.

It replaces the unstructured `config_context` keys these features used to live under with
real, query-able, REST/GraphQL-exposed columns. Each feature is a **per-device singleton
config** (one row per `dcim.Device`) plus **per-PORT child rows** that FK to `dcim.Interface`
— the per-interface overrides (an edge / BPDU-guard STP port, an LLDP tx-only port, a trusted
DHCP-snooping uplink) are the whole reason this is its own plugin, and they round-trip with
zero loss against the live switch config the `ansible-tofu` switch contract reconciles.

## Model

Six models, all inheriting `NetBoxModel` (custom fields, tags, change logging, GraphQL, REST):

| Model | Scope | Key fields |
|-------|-------|-----------|
| **STPConfig** | OneToOne `dcim.Device` | `enabled`, `mode` (stp/rstp/mstp), `priority` |
| **STPInterface** | OneToOne `dcim.Interface` | `priority`, `edge_port`, `bpdu_guard`, `root_guard` |
| **LLDPConfig** | OneToOne `dcim.Device` | `admin_status`, `transmit_interval`, `hold_multiplier` |
| **LLDPInterface** | OneToOne `dcim.Interface` | `admin_status` (per-port override) |
| **DHCPSnoopingConfig** | OneToOne `dcim.Device` | `enabled`, `vlans` (array of VLAN IDs) |
| **DHCPSnoopingInterface** | OneToOne `dcim.Interface` | `trusted` |

The OneToOne to `dcim.Device` / `dcim.Interface` makes each config a per-device singleton and
each override exactly one-per-port; deleting the device/interface cascades the L2 config away.

## Why

These L2 features have no home in NetBox core, so they were carried as free-form
`config_context` JSON — un-query-able, un-validated, with no per-port structure. This plugin
gives every key a real column with choice validation and a per-interface child table, so the
switch contract reads the config back 1:1 and a per-port edge/guard/trust state is a first-class,
filterable object instead of a buried JSON key.

## Install

```bash
uv pip install --python /opt/netbox/venv/bin/python netbox-data-link   # or: pip install -e .
# add "netbox_data_link" to PLUGINS in configuration.py
python manage.py migrate netbox_data_link
python manage.py collectstatic --no-input
systemctl restart netbox netbox-rq
```

## Develop / test

Tests run against a **real NetBox test database** (no mocks) via NetBox's Django test
framework. See `CLAUDE.md`.

```bash
python /opt/netbox/app/netbox/manage.py test netbox_data_link --keepdb -v2
```

## License

AGPL-3.0-or-later.
