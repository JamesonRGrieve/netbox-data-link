# SPDX-License-Identifier: AGPL-3.0-or-later
from dcim.models import Device, Interface
from django import forms
from netbox.forms import NetBoxModelFilterSetForm, NetBoxModelForm
from utilities.forms.fields import (
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
    NumericArrayField,
    TagFilterField,
)
from utilities.forms.rendering import FieldSet
from .choices import LLDPAdminStatusChoices, STPModeChoices
from .models import (
    DHCPSnoopingConfig,
    DHCPSnoopingInterface,
    LLDPConfig,
    LLDPInterface,
    STPConfig,
    STPInterface,
)


class STPConfigForm(NetBoxModelForm):
    device = DynamicModelChoiceField(queryset=Device.objects.all())

    fieldsets = (FieldSet("device", "enabled", "mode", "priority", name="STP"),)

    class Meta:
        model = STPConfig
        fields = ["device", "enabled", "mode", "priority", "tags"]


class STPInterfaceForm(NetBoxModelForm):
    interface = DynamicModelChoiceField(queryset=Interface.objects.all())

    fieldsets = (
        FieldSet("interface", "priority", name="Port"),
        FieldSet("edge_port", "bpdu_guard", "root_guard", name="Guards"),
    )

    class Meta:
        model = STPInterface
        fields = ["interface", "priority", "edge_port", "bpdu_guard", "root_guard", "tags"]


class LLDPConfigForm(NetBoxModelForm):
    device = DynamicModelChoiceField(queryset=Device.objects.all())

    fieldsets = (
        FieldSet("device", "admin_status", "transmit_interval", "hold_multiplier", name="LLDP"),
    )

    class Meta:
        model = LLDPConfig
        fields = ["device", "admin_status", "transmit_interval", "hold_multiplier", "tags"]


class LLDPInterfaceForm(NetBoxModelForm):
    interface = DynamicModelChoiceField(queryset=Interface.objects.all())

    fieldsets = (FieldSet("interface", "admin_status", name="Port"),)

    class Meta:
        model = LLDPInterface
        fields = ["interface", "admin_status", "tags"]


class DHCPSnoopingConfigForm(NetBoxModelForm):
    device = DynamicModelChoiceField(queryset=Device.objects.all())
    vlans = NumericArrayField(
        base_field=forms.IntegerField(),
        required=False,
        help_text="VLAN IDs DHCP snooping is enabled on, comma-separated or ranges (e.g. 10,20,30-40).",
    )

    fieldsets = (FieldSet("device", "enabled", "vlans", name="DHCP snooping"),)

    class Meta:
        model = DHCPSnoopingConfig
        fields = ["device", "enabled", "vlans", "tags"]


class DHCPSnoopingInterfaceForm(NetBoxModelForm):
    interface = DynamicModelChoiceField(queryset=Interface.objects.all())

    fieldsets = (FieldSet("interface", "trusted", name="Port"),)

    class Meta:
        model = DHCPSnoopingInterface
        fields = ["interface", "trusted", "tags"]


class STPConfigFilterForm(NetBoxModelFilterSetForm):
    model = STPConfig
    device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(), required=False, label="Device"
    )
    mode = forms.MultipleChoiceField(choices=STPModeChoices, required=False)
    enabled = forms.NullBooleanField(required=False)
    tag = TagFilterField(STPConfig)


class STPInterfaceFilterForm(NetBoxModelFilterSetForm):
    model = STPInterface
    interface_id = DynamicModelMultipleChoiceField(
        queryset=Interface.objects.all(), required=False, label="Interface"
    )
    device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(), required=False, label="Device"
    )
    edge_port = forms.NullBooleanField(required=False)
    bpdu_guard = forms.NullBooleanField(required=False)
    root_guard = forms.NullBooleanField(required=False)
    tag = TagFilterField(STPInterface)


class LLDPConfigFilterForm(NetBoxModelFilterSetForm):
    model = LLDPConfig
    device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(), required=False, label="Device"
    )
    admin_status = forms.MultipleChoiceField(choices=LLDPAdminStatusChoices, required=False)
    tag = TagFilterField(LLDPConfig)


class LLDPInterfaceFilterForm(NetBoxModelFilterSetForm):
    model = LLDPInterface
    interface_id = DynamicModelMultipleChoiceField(
        queryset=Interface.objects.all(), required=False, label="Interface"
    )
    device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(), required=False, label="Device"
    )
    admin_status = forms.MultipleChoiceField(choices=LLDPAdminStatusChoices, required=False)
    tag = TagFilterField(LLDPInterface)


class DHCPSnoopingConfigFilterForm(NetBoxModelFilterSetForm):
    model = DHCPSnoopingConfig
    device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(), required=False, label="Device"
    )
    enabled = forms.NullBooleanField(required=False)
    tag = TagFilterField(DHCPSnoopingConfig)


class DHCPSnoopingInterfaceFilterForm(NetBoxModelFilterSetForm):
    model = DHCPSnoopingInterface
    interface_id = DynamicModelMultipleChoiceField(
        queryset=Interface.objects.all(), required=False, label="Interface"
    )
    device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(), required=False, label="Device"
    )
    trusted = forms.NullBooleanField(required=False)
    tag = TagFilterField(DHCPSnoopingInterface)
