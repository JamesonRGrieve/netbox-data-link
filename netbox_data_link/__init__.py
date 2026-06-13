# SPDX-License-Identifier: AGPL-3.0-or-later
"""netbox-data-link: a native NetBox source of truth for a switch's **data-link
(OSI layer-2) control-plane features** — STP, LLDP, and DHCP snooping.

Replaces the unstructured ``config_context`` keys these features used to live under with
real, query-able, REST/GraphQL-exposed columns. Each feature is a per-device singleton
config (one row per ``dcim.Device``) plus per-PORT child rows that FK to ``dcim.Interface``
— the per-interface overrides (an edge/BPDU-guard STP port, an LLDP tx-only port, a trusted
DHCP-snooping uplink) are the whole reason this is its own plugin, and they round-trip with
zero loss against the live switch config the ansible-tofu switch contract reconciles.
"""

from netbox.plugins import PluginConfig

__version__ = "0.0.1"


class NetBoxDataLinkConfig(PluginConfig):
    name = "netbox_data_link"
    verbose_name = "NetBox Data Link"
    description = (
        "Native SoT for switch data-link (L2) control-plane features: STP, LLDP, DHCP snooping"
    )
    version = __version__
    author = "Jameson"
    base_url = "data-link"
    min_version = "4.6.0"
    max_version = "4.6.99"


config = NetBoxDataLinkConfig
