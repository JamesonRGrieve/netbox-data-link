# SPDX-License-Identifier: AGPL-3.0-or-later
"""FilterSet tests against a real DB (no mocks): device/interface scoping + choice filters."""

from dcim.models import Interface
from django.test import TestCase
from utilities.testing import create_test_device
from netbox_data_link.choices import LLDPAdminStatusChoices, STPModeChoices
from netbox_data_link.filtersets import (
    DHCPSnoopingConfigFilterSet,
    DHCPSnoopingInterfaceFilterSet,
    LLDPConfigFilterSet,
    LLDPInterfaceFilterSet,
    STPConfigFilterSet,
    STPInterfaceFilterSet,
)
from netbox_data_link.models import (
    DHCPSnoopingConfig,
    DHCPSnoopingInterface,
    LLDPConfig,
    LLDPInterface,
    STPConfig,
    STPInterface,
)


def _iface(device, name):
    return Interface.objects.create(device=device, name=name, type="1000base-t")


class STPConfigFilterSetTest(TestCase):
    queryset = STPConfig.objects.all()

    @classmethod
    def setUpTestData(cls):
        cls.d1 = create_test_device("sw1")
        cls.d2 = create_test_device("sw2")
        STPConfig.objects.create(device=cls.d1, mode=STPModeChoices.RSTP)
        STPConfig.objects.create(device=cls.d2, mode=STPModeChoices.MSTP)

    def test_device_id(self):
        self.assertEqual(
            STPConfigFilterSet({"device_id": [self.d1.pk]}, self.queryset).qs.count(), 1
        )

    def test_device_name(self):
        self.assertEqual(
            STPConfigFilterSet({"device": [self.d2.name]}, self.queryset).qs.count(), 1
        )

    def test_mode(self):
        self.assertEqual(
            STPConfigFilterSet({"mode": [STPModeChoices.MSTP]}, self.queryset).qs.count(), 1
        )


class STPInterfaceFilterSetTest(TestCase):
    queryset = STPInterface.objects.all()

    @classmethod
    def setUpTestData(cls):
        cls.d1 = create_test_device("sw1")
        cls.d2 = create_test_device("sw2")
        cls.i1 = _iface(cls.d1, "ge-0/0/1")
        cls.i2 = _iface(cls.d1, "ge-0/0/2")
        cls.i3 = _iface(cls.d2, "ge-0/0/1")
        STPInterface.objects.create(interface=cls.i1, edge_port=True, bpdu_guard=True)
        STPInterface.objects.create(interface=cls.i2, root_guard=True)
        STPInterface.objects.create(interface=cls.i3, edge_port=True)

    def test_interface_id(self):
        self.assertEqual(
            STPInterfaceFilterSet({"interface_id": [self.i1.pk]}, self.queryset).qs.count(), 1
        )

    def test_device_id_scopes_via_interface(self):
        self.assertEqual(self.queryset.count(), 3)
        self.assertEqual(
            STPInterfaceFilterSet({"device_id": [self.d1.pk]}, self.queryset).qs.count(), 2
        )
        self.assertEqual(
            STPInterfaceFilterSet({"device_id": [self.d2.pk]}, self.queryset).qs.count(), 1
        )

    def test_edge_port_and_guards(self):
        self.assertEqual(STPInterfaceFilterSet({"edge_port": True}, self.queryset).qs.count(), 2)
        self.assertEqual(STPInterfaceFilterSet({"root_guard": True}, self.queryset).qs.count(), 1)


class LLDPConfigFilterSetTest(TestCase):
    queryset = LLDPConfig.objects.all()

    @classmethod
    def setUpTestData(cls):
        cls.d1 = create_test_device("sw1")
        cls.d2 = create_test_device("sw2")
        LLDPConfig.objects.create(device=cls.d1, admin_status=LLDPAdminStatusChoices.ENABLED)
        LLDPConfig.objects.create(device=cls.d2, admin_status=LLDPAdminStatusChoices.TX_ONLY)

    def test_device_id(self):
        self.assertEqual(
            LLDPConfigFilterSet({"device_id": [self.d1.pk]}, self.queryset).qs.count(), 1
        )

    def test_admin_status(self):
        self.assertEqual(
            LLDPConfigFilterSet(
                {"admin_status": [LLDPAdminStatusChoices.TX_ONLY]}, self.queryset
            ).qs.count(),
            1,
        )


class LLDPInterfaceFilterSetTest(TestCase):
    queryset = LLDPInterface.objects.all()

    @classmethod
    def setUpTestData(cls):
        cls.d1 = create_test_device("sw1")
        cls.d2 = create_test_device("sw2")
        LLDPInterface.objects.create(
            interface=_iface(cls.d1, "ge-0/0/1"), admin_status=LLDPAdminStatusChoices.RX_ONLY
        )
        LLDPInterface.objects.create(
            interface=_iface(cls.d1, "ge-0/0/2"), admin_status=LLDPAdminStatusChoices.DISABLED
        )
        LLDPInterface.objects.create(
            interface=_iface(cls.d2, "ge-0/0/1"), admin_status=LLDPAdminStatusChoices.RX_ONLY
        )

    def test_device_id_scopes_via_interface(self):
        self.assertEqual(
            LLDPInterfaceFilterSet({"device_id": [self.d1.pk]}, self.queryset).qs.count(), 2
        )

    def test_admin_status(self):
        self.assertEqual(
            LLDPInterfaceFilterSet(
                {"admin_status": [LLDPAdminStatusChoices.RX_ONLY]}, self.queryset
            ).qs.count(),
            2,
        )


class DHCPSnoopingConfigFilterSetTest(TestCase):
    queryset = DHCPSnoopingConfig.objects.all()

    @classmethod
    def setUpTestData(cls):
        cls.d1 = create_test_device("sw1")
        cls.d2 = create_test_device("sw2")
        DHCPSnoopingConfig.objects.create(device=cls.d1, enabled=True, vlans=[10, 20])
        DHCPSnoopingConfig.objects.create(device=cls.d2, enabled=False)

    def test_device_id(self):
        self.assertEqual(
            DHCPSnoopingConfigFilterSet({"device_id": [self.d1.pk]}, self.queryset).qs.count(), 1
        )

    def test_enabled(self):
        self.assertEqual(
            DHCPSnoopingConfigFilterSet({"enabled": True}, self.queryset).qs.count(), 1
        )


class DHCPSnoopingInterfaceFilterSetTest(TestCase):
    queryset = DHCPSnoopingInterface.objects.all()

    @classmethod
    def setUpTestData(cls):
        cls.d1 = create_test_device("sw1")
        cls.d2 = create_test_device("sw2")
        DHCPSnoopingInterface.objects.create(interface=_iface(cls.d1, "ge-0/0/1"), trusted=True)
        DHCPSnoopingInterface.objects.create(interface=_iface(cls.d1, "ge-0/0/2"), trusted=False)
        DHCPSnoopingInterface.objects.create(interface=_iface(cls.d2, "ge-0/0/1"), trusted=True)

    def test_interface_id(self):
        target = DHCPSnoopingInterface.objects.first()
        self.assertEqual(
            DHCPSnoopingInterfaceFilterSet(
                {"interface_id": [target.interface_id]}, self.queryset
            ).qs.count(),
            1,
        )

    def test_device_id_scopes_via_interface(self):
        self.assertEqual(
            DHCPSnoopingInterfaceFilterSet({"device_id": [self.d1.pk]}, self.queryset).qs.count(), 2
        )

    def test_trusted(self):
        self.assertEqual(
            DHCPSnoopingInterfaceFilterSet({"trusted": True}, self.queryset).qs.count(), 2
        )
