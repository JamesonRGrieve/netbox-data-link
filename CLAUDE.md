# netbox-data-link — Agent Operating Guide

Adapted from `../netbox-pf`'s `CLAUDE.md` (same engineering + test discipline), re-targeted
from pf firewall rules to a switch's **data-link (OSI layer-2) control plane**.

`netbox-data-link` is an **AGPL-3.0** NetBox 4.6 Django plugin: a **native source of truth for
STP, LLDP, and DHCP snooping** on a switch. It replaces the unstructured `config_context` keys
these features used to live under with real columns — choice-validated, query-able, and exposed
over REST/GraphQL. Each feature is a **per-device singleton** (OneToOne to `dcim.Device`) plus
**per-PORT child rows** (OneToOne to `dcim.Interface`); the per-interface overrides are the whole
reason this is its own plugin, and they round-trip with zero loss against the live switch config
the `ansible-tofu` switch contract reconciles.

---

## Key Directives / Rules

### DO, ALWAYS:
- If functionality won't work without a parameter, make it a **required positional** parameter —
  never an optional one with an inline presence check.
- Any time you modify a source file, ensure its accompanying test under `netbox_data_link/tests/`
  contains **comprehensive tests for the change WITHOUT MOCKS**, so `manage.py test
  netbox_data_link` discovers them, and update any `.md` in the same directory that references
  the changed code.
- Write concise code (avoid obvious comments; use one-liners where possible).
- Critically analyze requirements and ask all necessary clarifying questions before implementing
  or refactoring.
- Phrase documentation for yourself (AI) and for autistic/ADHD humans: a clear architectural
  summary you could reconstruct the code from with 95% accuracy, with minimal snippets — **not**
  usage examples (the browsable REST/GraphQL schema is the usage reference).

### DO NOT, EVER, UNDER ANY CIRCUMSTANCE:
- Make assumptions, or answer with "is likely", "probably", or "might be".
- Use frame-local or thread-local state instead of passing data via parameters.
- Skip a failing test instead of fixing the root cause.
- Fix broken functionality while keeping the broken path as a fallback.
- Re-implement existing functionality in a second location to bypass the original.
- Use bandaid fixes instead of fixing the core functionality.
- **Mock the database, the ORM, the NetBox API test client, or any integration path.** Tests run
  against a **real test database** via NetBox's Django test framework — use real model instances
  and real API requests. Only pure utility functions may use mocks for isolation.

### Python / Django Guidelines:
- Import children of `datetime`: `from datetime import date` — **never** `import datetime` then
  `datetime.date`.
- Imports are package-relative inside `netbox_data_link` (`from .models import STPConfig`), never
  `from netbox_data_link.models import ...`.
- Models inherit `netbox.models.NetBoxModel` (custom fields, tags, journaling, change logging,
  GraphQL — for free).
- **SPDX header on every source file**: `# SPDX-License-Identifier: AGPL-3.0-or-later`.

### Documentation Guidelines:
- Markdown docs are concise: reconstruct-the-code-with-95%-accuracy architectural summaries with
  minimal snippets, not usage tutorials.

---

## Architecture (NetBox 4.6 plugin)

| File | Responsibility |
|------|----------------|
| `__init__.py` | `PluginConfig` — name `netbox_data_link`, `base_url='data-link'`, min/max NetBox version |
| `choices.py` | `ChoiceSet`s: STP mode, LLDP admin-status |
| `models.py` | The six L2 models (see §Model) |
| `migrations/` | schema migrations — hand-authored (NetBox disables `makemigrations` in prod); verify with `makemigrations --check --dry-run` on an ephemeral NetBox |
| `api/serializers.py`, `api/views.py`, `api/urls.py` | REST API (`NetBoxModelViewSet`) — the contract `ansible-tofu` reads |
| `filtersets.py` | `NetBoxModelFilterSet` per model (drives API + UI filtering); filter by device + interface |
| `tables.py`, `forms.py`, `navigation.py`, `views.py`, `urls.py` | UI layer |
| `graphql/` | GraphQL types (none shipped yet — `NetBoxModel` still exposes auto GraphQL) |

### Model — the L2 SoT (per-device singleton + per-port child)
- **STPConfig** (OneToOne `Device`): `enabled`, `mode` (stp/rstp/mstp), `priority`.
- **STPInterface** (OneToOne `Interface`): `priority`, `edge_port`, `bpdu_guard`, `root_guard`.
- **LLDPConfig** (OneToOne `Device`): `admin_status`, `transmit_interval`, `hold_multiplier`.
- **LLDPInterface** (OneToOne `Interface`): `admin_status` (per-port override).
- **DHCPSnoopingConfig** (OneToOne `Device`): `enabled`, `vlans` (`ArrayField` of VLAN IDs).
- **DHCPSnoopingInterface** (OneToOne `Interface`): `trusted`.

The OneToOne to `Device`/`Interface` is what enforces "one config per device" and "one override
per port" at the DB level (the OneToOne unique index); `on_delete=CASCADE` drops the L2 config
when the device/interface goes away.

---

## Testing (NO MOCKS — real DB, NetBox test framework)

- Tests live in `netbox_data_link/tests/` (inside the package, so `manage.py test
  netbox_data_link` discovers them and they ship with the plugin), one module per source module
  (`test_models.py`, `test_api.py`, `test_filtersets.py`).
- Use NetBox's base classes from `utilities.testing`: `APIViewTestCases.APIViewTestCase` (composed
  CRUD mixins), `create_test_device`. Per-port models need a real `dcim.Interface` per object
  (`Interface.objects.create(device=..., name=..., type="1000base-t")`); OneToOne configs need a
  fresh device/interface per created object.
- **Test isolation**: Django wraps each test in a transaction against a per-run test database with
  automatic teardown.
- **Never skip a failing test** — fix the root cause; repair deficiencies starting with the
  lowest-hanging fruit.
- **Run**: `python /opt/netbox/app/netbox/manage.py test netbox_data_link --keepdb -v2` (or
  `pytest` with `pytest-django` + `DJANGO_SETTINGS_MODULE=netbox.settings`).
- **Coverage bar**: every model, serializer, filterset, and view has tests — including the
  per-interface child models (uniqueness, CASCADE, scoping by device-through-interface).

---

## Licensing
- **AGPL-3.0-or-later** (workspace production-IaC standard). SPDX header in every file.
