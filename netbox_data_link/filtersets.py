# SPDX-License-Identifier: AGPL-3.0-or-later
import django_filters
from dcim.models import Device, Interface
from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet
from .choices import LLDPAdminStatusChoices, STPModeChoices
from .models import (
    DHCPSnoopingConfig,
    DHCPSnoopingInterface,
    LLDPConfig,
    LLDPInterface,
    STPConfig,
    STPInterface,
)


# Explicit FK filters: django-filter does NOT derive `<fk>_id` from a bare FK/OneToOne in
# Meta.fields, so a bare `device`/`interface` would be silently ignored. NetBox convention is
# `<fk>_id` (by PK) + `<fk>` (by natural key).
class _DeviceFilterMixin(django_filters.FilterSet):
    device_id = django_filters.ModelMultipleChoiceFilter(
        field_name="device", queryset=Device.objects.all(), label="Device (ID)"
    )
    device = django_filters.ModelMultipleChoiceFilter(
        field_name="device__name",
        to_field_name="name",
        queryset=Device.objects.all(),
        label="Device (name)",
    )


class _InterfaceFilterMixin(django_filters.FilterSet):
    interface_id = django_filters.ModelMultipleChoiceFilter(
        field_name="interface", queryset=Interface.objects.all(), label="Interface (ID)"
    )
    device_id = django_filters.ModelMultipleChoiceFilter(
        field_name="interface__device", queryset=Device.objects.all(), label="Device (ID)"
    )


class STPConfigFilterSet(_DeviceFilterMixin, NetBoxModelFilterSet):
    mode = django_filters.MultipleChoiceFilter(choices=STPModeChoices)

    class Meta:
        model = STPConfig
        fields = ["id", "enabled", "priority"]

    def search(self, queryset, name, value):
        return queryset.filter(Q(device__name__icontains=value))


class STPInterfaceFilterSet(_InterfaceFilterMixin, NetBoxModelFilterSet):
    class Meta:
        model = STPInterface
        fields = ["id", "priority", "edge_port", "bpdu_guard", "root_guard"]

    def search(self, queryset, name, value):
        return queryset.filter(Q(interface__name__icontains=value))


class LLDPConfigFilterSet(_DeviceFilterMixin, NetBoxModelFilterSet):
    admin_status = django_filters.MultipleChoiceFilter(choices=LLDPAdminStatusChoices)

    class Meta:
        model = LLDPConfig
        fields = ["id", "transmit_interval", "hold_multiplier"]

    def search(self, queryset, name, value):
        return queryset.filter(Q(device__name__icontains=value))


class LLDPInterfaceFilterSet(_InterfaceFilterMixin, NetBoxModelFilterSet):
    admin_status = django_filters.MultipleChoiceFilter(choices=LLDPAdminStatusChoices)

    class Meta:
        model = LLDPInterface
        fields = ["id"]

    def search(self, queryset, name, value):
        return queryset.filter(Q(interface__name__icontains=value))


class DHCPSnoopingConfigFilterSet(_DeviceFilterMixin, NetBoxModelFilterSet):
    class Meta:
        model = DHCPSnoopingConfig
        fields = ["id", "enabled"]

    def search(self, queryset, name, value):
        return queryset.filter(Q(device__name__icontains=value))


class DHCPSnoopingInterfaceFilterSet(_InterfaceFilterMixin, NetBoxModelFilterSet):
    class Meta:
        model = DHCPSnoopingInterface
        fields = ["id", "trusted"]

    def search(self, queryset, name, value):
        return queryset.filter(Q(interface__name__icontains=value))
