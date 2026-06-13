# SPDX-License-Identifier: AGPL-3.0-or-later
from netbox.api.viewsets import NetBoxModelViewSet
from .. import filtersets
from ..models import (
    DHCPSnoopingConfig,
    DHCPSnoopingInterface,
    LLDPConfig,
    LLDPInterface,
    STPConfig,
    STPInterface,
)
from .serializers import (
    DHCPSnoopingConfigSerializer,
    DHCPSnoopingInterfaceSerializer,
    LLDPConfigSerializer,
    LLDPInterfaceSerializer,
    STPConfigSerializer,
    STPInterfaceSerializer,
)


class STPConfigViewSet(NetBoxModelViewSet):
    queryset = STPConfig.objects.prefetch_related("device", "tags")
    serializer_class = STPConfigSerializer
    filterset_class = filtersets.STPConfigFilterSet


class STPInterfaceViewSet(NetBoxModelViewSet):
    queryset = STPInterface.objects.prefetch_related("interface", "tags")
    serializer_class = STPInterfaceSerializer
    filterset_class = filtersets.STPInterfaceFilterSet


class LLDPConfigViewSet(NetBoxModelViewSet):
    queryset = LLDPConfig.objects.prefetch_related("device", "tags")
    serializer_class = LLDPConfigSerializer
    filterset_class = filtersets.LLDPConfigFilterSet


class LLDPInterfaceViewSet(NetBoxModelViewSet):
    queryset = LLDPInterface.objects.prefetch_related("interface", "tags")
    serializer_class = LLDPInterfaceSerializer
    filterset_class = filtersets.LLDPInterfaceFilterSet


class DHCPSnoopingConfigViewSet(NetBoxModelViewSet):
    queryset = DHCPSnoopingConfig.objects.prefetch_related("device", "tags")
    serializer_class = DHCPSnoopingConfigSerializer
    filterset_class = filtersets.DHCPSnoopingConfigFilterSet


class DHCPSnoopingInterfaceViewSet(NetBoxModelViewSet):
    queryset = DHCPSnoopingInterface.objects.prefetch_related("interface", "tags")
    serializer_class = DHCPSnoopingInterfaceSerializer
    filterset_class = filtersets.DHCPSnoopingInterfaceFilterSet
