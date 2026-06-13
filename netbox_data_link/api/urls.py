# SPDX-License-Identifier: AGPL-3.0-or-later
from netbox.api.routers import NetBoxRouter
from . import views

app_name = "netbox_data_link"

router = NetBoxRouter()
router.register("stp-configs", views.STPConfigViewSet)
router.register("stp-interfaces", views.STPInterfaceViewSet)
router.register("lldp-configs", views.LLDPConfigViewSet)
router.register("lldp-interfaces", views.LLDPInterfaceViewSet)
router.register("dhcp-snooping-configs", views.DHCPSnoopingConfigViewSet)
router.register("dhcp-snooping-interfaces", views.DHCPSnoopingInterfaceViewSet)

urlpatterns = router.urls
