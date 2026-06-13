# SPDX-License-Identifier: AGPL-3.0-or-later
import django_tables2 as tables
from netbox.tables import NetBoxTable, columns
from .models import (
    DHCPSnoopingConfig,
    DHCPSnoopingInterface,
    LLDPConfig,
    LLDPInterface,
    STPConfig,
    STPInterface,
)


class STPConfigTable(NetBoxTable):
    device = tables.Column(linkify=True)
    mode = columns.ChoiceFieldColumn()
    tags = columns.TagColumn(url_name="plugins:netbox_data_link:stpconfig_list")

    class Meta(NetBoxTable.Meta):
        model = STPConfig
        fields = (
            "pk",
            "id",
            "device",
            "enabled",
            "mode",
            "priority",
            "tags",
            "created",
            "last_updated",
        )
        default_columns = ("device", "enabled", "mode", "priority")


class STPInterfaceTable(NetBoxTable):
    interface = tables.Column(linkify=True)
    tags = columns.TagColumn(url_name="plugins:netbox_data_link:stpinterface_list")

    class Meta(NetBoxTable.Meta):
        model = STPInterface
        fields = (
            "pk",
            "id",
            "interface",
            "priority",
            "edge_port",
            "bpdu_guard",
            "root_guard",
            "tags",
            "created",
            "last_updated",
        )
        default_columns = ("interface", "priority", "edge_port", "bpdu_guard", "root_guard")


class LLDPConfigTable(NetBoxTable):
    device = tables.Column(linkify=True)
    admin_status = columns.ChoiceFieldColumn()
    tags = columns.TagColumn(url_name="plugins:netbox_data_link:lldpconfig_list")

    class Meta(NetBoxTable.Meta):
        model = LLDPConfig
        fields = (
            "pk",
            "id",
            "device",
            "admin_status",
            "transmit_interval",
            "hold_multiplier",
            "tags",
            "created",
            "last_updated",
        )
        default_columns = ("device", "admin_status", "transmit_interval", "hold_multiplier")


class LLDPInterfaceTable(NetBoxTable):
    interface = tables.Column(linkify=True)
    admin_status = columns.ChoiceFieldColumn()
    tags = columns.TagColumn(url_name="plugins:netbox_data_link:lldpinterface_list")

    class Meta(NetBoxTable.Meta):
        model = LLDPInterface
        fields = ("pk", "id", "interface", "admin_status", "tags", "created", "last_updated")
        default_columns = ("interface", "admin_status")


class DHCPSnoopingConfigTable(NetBoxTable):
    device = tables.Column(linkify=True)
    tags = columns.TagColumn(url_name="plugins:netbox_data_link:dhcpsnoopingconfig_list")

    class Meta(NetBoxTable.Meta):
        model = DHCPSnoopingConfig
        fields = ("pk", "id", "device", "enabled", "vlans", "tags", "created", "last_updated")
        default_columns = ("device", "enabled", "vlans")


class DHCPSnoopingInterfaceTable(NetBoxTable):
    interface = tables.Column(linkify=True)
    tags = columns.TagColumn(url_name="plugins:netbox_data_link:dhcpsnoopinginterface_list")

    class Meta(NetBoxTable.Meta):
        model = DHCPSnoopingInterface
        fields = ("pk", "id", "interface", "trusted", "tags", "created", "last_updated")
        default_columns = ("interface", "trusted")
