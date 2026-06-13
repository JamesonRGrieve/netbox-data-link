# SPDX-License-Identifier: AGPL-3.0-or-later
from dcim.api.serializers import DeviceSerializer, InterfaceSerializer
from netbox.api.serializers import NetBoxModelSerializer
from rest_framework import serializers
from ..models import (
    DHCPSnoopingConfig,
    DHCPSnoopingInterface,
    LLDPConfig,
    LLDPInterface,
    STPConfig,
    STPInterface,
)


class STPConfigSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_data_link-api:stpconfig-detail"
    )
    device = DeviceSerializer(nested=True)

    class Meta:
        model = STPConfig
        fields = [
            "id",
            "url",
            "display",
            "device",
            "enabled",
            "mode",
            "priority",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        ]
        brief_fields = ["id", "url", "display", "device", "mode"]


class STPInterfaceSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_data_link-api:stpinterface-detail"
    )
    interface = InterfaceSerializer(nested=True)

    class Meta:
        model = STPInterface
        fields = [
            "id",
            "url",
            "display",
            "interface",
            "priority",
            "edge_port",
            "bpdu_guard",
            "root_guard",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        ]
        brief_fields = ["id", "url", "display", "interface"]


class LLDPConfigSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_data_link-api:lldpconfig-detail"
    )
    device = DeviceSerializer(nested=True)

    class Meta:
        model = LLDPConfig
        fields = [
            "id",
            "url",
            "display",
            "device",
            "admin_status",
            "transmit_interval",
            "hold_multiplier",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        ]
        brief_fields = ["id", "url", "display", "device", "admin_status"]


class LLDPInterfaceSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_data_link-api:lldpinterface-detail"
    )
    interface = InterfaceSerializer(nested=True)

    class Meta:
        model = LLDPInterface
        fields = [
            "id",
            "url",
            "display",
            "interface",
            "admin_status",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        ]
        brief_fields = ["id", "url", "display", "interface", "admin_status"]


class DHCPSnoopingConfigSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_data_link-api:dhcpsnoopingconfig-detail"
    )
    device = DeviceSerializer(nested=True)

    class Meta:
        model = DHCPSnoopingConfig
        fields = [
            "id",
            "url",
            "display",
            "device",
            "enabled",
            "vlans",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        ]
        brief_fields = ["id", "url", "display", "device"]


class DHCPSnoopingInterfaceSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_data_link-api:dhcpsnoopinginterface-detail"
    )
    interface = InterfaceSerializer(nested=True)

    class Meta:
        model = DHCPSnoopingInterface
        fields = [
            "id",
            "url",
            "display",
            "interface",
            "trusted",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        ]
        brief_fields = ["id", "url", "display", "interface", "trusted"]
