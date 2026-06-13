# SPDX-License-Identifier: AGPL-3.0-or-later
from django.urls import path
from netbox.views.generic import ObjectChangeLogView, ObjectJournalView
from . import models, views

urlpatterns = [
    # STP configs
    path("stp-configs/", views.STPConfigListView.as_view(), name="stpconfig_list"),
    path("stp-configs/add/", views.STPConfigEditView.as_view(), name="stpconfig_add"),
    path(
        "stp-configs/delete/", views.STPConfigBulkDeleteView.as_view(), name="stpconfig_bulk_delete"
    ),
    path("stp-configs/<int:pk>/", views.STPConfigView.as_view(), name="stpconfig"),
    path("stp-configs/<int:pk>/edit/", views.STPConfigEditView.as_view(), name="stpconfig_edit"),
    path(
        "stp-configs/<int:pk>/delete/", views.STPConfigDeleteView.as_view(), name="stpconfig_delete"
    ),
    path(
        "stp-configs/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="stpconfig_changelog",
        kwargs={"model": models.STPConfig},
    ),
    path(
        "stp-configs/<int:pk>/journal/",
        ObjectJournalView.as_view(),
        name="stpconfig_journal",
        kwargs={"model": models.STPConfig},
    ),
    # STP interfaces
    path("stp-interfaces/", views.STPInterfaceListView.as_view(), name="stpinterface_list"),
    path("stp-interfaces/add/", views.STPInterfaceEditView.as_view(), name="stpinterface_add"),
    path(
        "stp-interfaces/delete/",
        views.STPInterfaceBulkDeleteView.as_view(),
        name="stpinterface_bulk_delete",
    ),
    path("stp-interfaces/<int:pk>/", views.STPInterfaceView.as_view(), name="stpinterface"),
    path(
        "stp-interfaces/<int:pk>/edit/",
        views.STPInterfaceEditView.as_view(),
        name="stpinterface_edit",
    ),
    path(
        "stp-interfaces/<int:pk>/delete/",
        views.STPInterfaceDeleteView.as_view(),
        name="stpinterface_delete",
    ),
    path(
        "stp-interfaces/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="stpinterface_changelog",
        kwargs={"model": models.STPInterface},
    ),
    path(
        "stp-interfaces/<int:pk>/journal/",
        ObjectJournalView.as_view(),
        name="stpinterface_journal",
        kwargs={"model": models.STPInterface},
    ),
    # LLDP configs
    path("lldp-configs/", views.LLDPConfigListView.as_view(), name="lldpconfig_list"),
    path("lldp-configs/add/", views.LLDPConfigEditView.as_view(), name="lldpconfig_add"),
    path(
        "lldp-configs/delete/",
        views.LLDPConfigBulkDeleteView.as_view(),
        name="lldpconfig_bulk_delete",
    ),
    path("lldp-configs/<int:pk>/", views.LLDPConfigView.as_view(), name="lldpconfig"),
    path("lldp-configs/<int:pk>/edit/", views.LLDPConfigEditView.as_view(), name="lldpconfig_edit"),
    path(
        "lldp-configs/<int:pk>/delete/",
        views.LLDPConfigDeleteView.as_view(),
        name="lldpconfig_delete",
    ),
    path(
        "lldp-configs/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="lldpconfig_changelog",
        kwargs={"model": models.LLDPConfig},
    ),
    path(
        "lldp-configs/<int:pk>/journal/",
        ObjectJournalView.as_view(),
        name="lldpconfig_journal",
        kwargs={"model": models.LLDPConfig},
    ),
    # LLDP interfaces
    path("lldp-interfaces/", views.LLDPInterfaceListView.as_view(), name="lldpinterface_list"),
    path("lldp-interfaces/add/", views.LLDPInterfaceEditView.as_view(), name="lldpinterface_add"),
    path(
        "lldp-interfaces/delete/",
        views.LLDPInterfaceBulkDeleteView.as_view(),
        name="lldpinterface_bulk_delete",
    ),
    path("lldp-interfaces/<int:pk>/", views.LLDPInterfaceView.as_view(), name="lldpinterface"),
    path(
        "lldp-interfaces/<int:pk>/edit/",
        views.LLDPInterfaceEditView.as_view(),
        name="lldpinterface_edit",
    ),
    path(
        "lldp-interfaces/<int:pk>/delete/",
        views.LLDPInterfaceDeleteView.as_view(),
        name="lldpinterface_delete",
    ),
    path(
        "lldp-interfaces/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="lldpinterface_changelog",
        kwargs={"model": models.LLDPInterface},
    ),
    path(
        "lldp-interfaces/<int:pk>/journal/",
        ObjectJournalView.as_view(),
        name="lldpinterface_journal",
        kwargs={"model": models.LLDPInterface},
    ),
    # DHCP snooping configs
    path(
        "dhcp-snooping-configs/",
        views.DHCPSnoopingConfigListView.as_view(),
        name="dhcpsnoopingconfig_list",
    ),
    path(
        "dhcp-snooping-configs/add/",
        views.DHCPSnoopingConfigEditView.as_view(),
        name="dhcpsnoopingconfig_add",
    ),
    path(
        "dhcp-snooping-configs/delete/",
        views.DHCPSnoopingConfigBulkDeleteView.as_view(),
        name="dhcpsnoopingconfig_bulk_delete",
    ),
    path(
        "dhcp-snooping-configs/<int:pk>/",
        views.DHCPSnoopingConfigView.as_view(),
        name="dhcpsnoopingconfig",
    ),
    path(
        "dhcp-snooping-configs/<int:pk>/edit/",
        views.DHCPSnoopingConfigEditView.as_view(),
        name="dhcpsnoopingconfig_edit",
    ),
    path(
        "dhcp-snooping-configs/<int:pk>/delete/",
        views.DHCPSnoopingConfigDeleteView.as_view(),
        name="dhcpsnoopingconfig_delete",
    ),
    path(
        "dhcp-snooping-configs/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="dhcpsnoopingconfig_changelog",
        kwargs={"model": models.DHCPSnoopingConfig},
    ),
    path(
        "dhcp-snooping-configs/<int:pk>/journal/",
        ObjectJournalView.as_view(),
        name="dhcpsnoopingconfig_journal",
        kwargs={"model": models.DHCPSnoopingConfig},
    ),
    # DHCP snooping interfaces
    path(
        "dhcp-snooping-interfaces/",
        views.DHCPSnoopingInterfaceListView.as_view(),
        name="dhcpsnoopinginterface_list",
    ),
    path(
        "dhcp-snooping-interfaces/add/",
        views.DHCPSnoopingInterfaceEditView.as_view(),
        name="dhcpsnoopinginterface_add",
    ),
    path(
        "dhcp-snooping-interfaces/delete/",
        views.DHCPSnoopingInterfaceBulkDeleteView.as_view(),
        name="dhcpsnoopinginterface_bulk_delete",
    ),
    path(
        "dhcp-snooping-interfaces/<int:pk>/",
        views.DHCPSnoopingInterfaceView.as_view(),
        name="dhcpsnoopinginterface",
    ),
    path(
        "dhcp-snooping-interfaces/<int:pk>/edit/",
        views.DHCPSnoopingInterfaceEditView.as_view(),
        name="dhcpsnoopinginterface_edit",
    ),
    path(
        "dhcp-snooping-interfaces/<int:pk>/delete/",
        views.DHCPSnoopingInterfaceDeleteView.as_view(),
        name="dhcpsnoopinginterface_delete",
    ),
    path(
        "dhcp-snooping-interfaces/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="dhcpsnoopinginterface_changelog",
        kwargs={"model": models.DHCPSnoopingInterface},
    ),
    path(
        "dhcp-snooping-interfaces/<int:pk>/journal/",
        ObjectJournalView.as_view(),
        name="dhcpsnoopinginterface_journal",
        kwargs={"model": models.DHCPSnoopingInterface},
    ),
]
