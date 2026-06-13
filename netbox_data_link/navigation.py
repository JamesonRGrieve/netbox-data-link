# SPDX-License-Identifier: AGPL-3.0-or-later
from netbox.plugins import PluginMenu, PluginMenuButton, PluginMenuItem

_stp = PluginMenuItem(
    link="plugins:netbox_data_link:stpconfig_list",
    link_text="STP Configs",
    buttons=[
        PluginMenuButton("plugins:netbox_data_link:stpconfig_add", "Add", "mdi mdi-plus-thick")
    ],
)
_stp_if = PluginMenuItem(
    link="plugins:netbox_data_link:stpinterface_list",
    link_text="STP Interfaces",
    buttons=[
        PluginMenuButton("plugins:netbox_data_link:stpinterface_add", "Add", "mdi mdi-plus-thick")
    ],
)
_lldp = PluginMenuItem(
    link="plugins:netbox_data_link:lldpconfig_list",
    link_text="LLDP Configs",
    buttons=[
        PluginMenuButton("plugins:netbox_data_link:lldpconfig_add", "Add", "mdi mdi-plus-thick")
    ],
)
_lldp_if = PluginMenuItem(
    link="plugins:netbox_data_link:lldpinterface_list",
    link_text="LLDP Interfaces",
    buttons=[
        PluginMenuButton("plugins:netbox_data_link:lldpinterface_add", "Add", "mdi mdi-plus-thick")
    ],
)
_dhcp = PluginMenuItem(
    link="plugins:netbox_data_link:dhcpsnoopingconfig_list",
    link_text="DHCP Snooping Configs",
    buttons=[
        PluginMenuButton(
            "plugins:netbox_data_link:dhcpsnoopingconfig_add", "Add", "mdi mdi-plus-thick"
        )
    ],
)
_dhcp_if = PluginMenuItem(
    link="plugins:netbox_data_link:dhcpsnoopinginterface_list",
    link_text="DHCP Snooping Interfaces",
    buttons=[
        PluginMenuButton(
            "plugins:netbox_data_link:dhcpsnoopinginterface_add", "Add", "mdi mdi-plus-thick"
        )
    ],
)

menu = PluginMenu(
    label="Data Link (L2)",
    groups=(
        ("Spanning Tree", (_stp, _stp_if)),
        ("LLDP", (_lldp, _lldp_if)),
        ("DHCP Snooping", (_dhcp, _dhcp_if)),
    ),
    icon_class="mdi mdi-lan",
)
