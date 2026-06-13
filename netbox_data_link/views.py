# SPDX-License-Identifier: AGPL-3.0-or-later
from netbox.views import generic
from . import filtersets, forms, models, tables


class STPConfigView(generic.ObjectView):
    queryset = models.STPConfig.objects.all()


class STPConfigListView(generic.ObjectListView):
    queryset = models.STPConfig.objects.all()
    table = tables.STPConfigTable
    filterset = filtersets.STPConfigFilterSet
    filterset_form = forms.STPConfigFilterForm


class STPConfigEditView(generic.ObjectEditView):
    queryset = models.STPConfig.objects.all()
    form = forms.STPConfigForm


class STPConfigDeleteView(generic.ObjectDeleteView):
    queryset = models.STPConfig.objects.all()


class STPConfigBulkDeleteView(generic.BulkDeleteView):
    queryset = models.STPConfig.objects.all()
    table = tables.STPConfigTable


class STPInterfaceView(generic.ObjectView):
    queryset = models.STPInterface.objects.all()


class STPInterfaceListView(generic.ObjectListView):
    queryset = models.STPInterface.objects.all()
    table = tables.STPInterfaceTable
    filterset = filtersets.STPInterfaceFilterSet
    filterset_form = forms.STPInterfaceFilterForm


class STPInterfaceEditView(generic.ObjectEditView):
    queryset = models.STPInterface.objects.all()
    form = forms.STPInterfaceForm


class STPInterfaceDeleteView(generic.ObjectDeleteView):
    queryset = models.STPInterface.objects.all()


class STPInterfaceBulkDeleteView(generic.BulkDeleteView):
    queryset = models.STPInterface.objects.all()
    table = tables.STPInterfaceTable


class LLDPConfigView(generic.ObjectView):
    queryset = models.LLDPConfig.objects.all()


class LLDPConfigListView(generic.ObjectListView):
    queryset = models.LLDPConfig.objects.all()
    table = tables.LLDPConfigTable
    filterset = filtersets.LLDPConfigFilterSet
    filterset_form = forms.LLDPConfigFilterForm


class LLDPConfigEditView(generic.ObjectEditView):
    queryset = models.LLDPConfig.objects.all()
    form = forms.LLDPConfigForm


class LLDPConfigDeleteView(generic.ObjectDeleteView):
    queryset = models.LLDPConfig.objects.all()


class LLDPConfigBulkDeleteView(generic.BulkDeleteView):
    queryset = models.LLDPConfig.objects.all()
    table = tables.LLDPConfigTable


class LLDPInterfaceView(generic.ObjectView):
    queryset = models.LLDPInterface.objects.all()


class LLDPInterfaceListView(generic.ObjectListView):
    queryset = models.LLDPInterface.objects.all()
    table = tables.LLDPInterfaceTable
    filterset = filtersets.LLDPInterfaceFilterSet
    filterset_form = forms.LLDPInterfaceFilterForm


class LLDPInterfaceEditView(generic.ObjectEditView):
    queryset = models.LLDPInterface.objects.all()
    form = forms.LLDPInterfaceForm


class LLDPInterfaceDeleteView(generic.ObjectDeleteView):
    queryset = models.LLDPInterface.objects.all()


class LLDPInterfaceBulkDeleteView(generic.BulkDeleteView):
    queryset = models.LLDPInterface.objects.all()
    table = tables.LLDPInterfaceTable


class DHCPSnoopingConfigView(generic.ObjectView):
    queryset = models.DHCPSnoopingConfig.objects.all()


class DHCPSnoopingConfigListView(generic.ObjectListView):
    queryset = models.DHCPSnoopingConfig.objects.all()
    table = tables.DHCPSnoopingConfigTable
    filterset = filtersets.DHCPSnoopingConfigFilterSet
    filterset_form = forms.DHCPSnoopingConfigFilterForm


class DHCPSnoopingConfigEditView(generic.ObjectEditView):
    queryset = models.DHCPSnoopingConfig.objects.all()
    form = forms.DHCPSnoopingConfigForm


class DHCPSnoopingConfigDeleteView(generic.ObjectDeleteView):
    queryset = models.DHCPSnoopingConfig.objects.all()


class DHCPSnoopingConfigBulkDeleteView(generic.BulkDeleteView):
    queryset = models.DHCPSnoopingConfig.objects.all()
    table = tables.DHCPSnoopingConfigTable


class DHCPSnoopingInterfaceView(generic.ObjectView):
    queryset = models.DHCPSnoopingInterface.objects.all()


class DHCPSnoopingInterfaceListView(generic.ObjectListView):
    queryset = models.DHCPSnoopingInterface.objects.all()
    table = tables.DHCPSnoopingInterfaceTable
    filterset = filtersets.DHCPSnoopingInterfaceFilterSet
    filterset_form = forms.DHCPSnoopingInterfaceFilterForm


class DHCPSnoopingInterfaceEditView(generic.ObjectEditView):
    queryset = models.DHCPSnoopingInterface.objects.all()
    form = forms.DHCPSnoopingInterfaceForm


class DHCPSnoopingInterfaceDeleteView(generic.ObjectDeleteView):
    queryset = models.DHCPSnoopingInterface.objects.all()


class DHCPSnoopingInterfaceBulkDeleteView(generic.BulkDeleteView):
    queryset = models.DHCPSnoopingInterface.objects.all()
    table = tables.DHCPSnoopingInterfaceTable
