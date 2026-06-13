# SPDX-License-Identifier: AGPL-3.0-or-later
"""Model tests against a real DB (no mocks): creation, str/url/color, the OneToOne
"one row per device / per interface" constraint, CASCADE behaviour, ArrayField round-trip."""

from dcim.models import Interface
from django.db import transaction
from django.db.utils import IntegrityError
from django.test import TestCase
from utilities.testing import create_test_device
from netbox_data_link.choices import LLDPAdminStatusChoices, STPModeChoices
from netbox_data_link.models import (
    DHCPSnoopingConfig,
    DHCPSnoopingInterface,
    LLDPConfig,
    LLDPInterface,
    STPConfig,
    STPInterface,
)


def _make_interface(device, name):
    return Interface.objects.create(device=device, name=name, type="1000base-t")


class STPConfigModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.device = create_test_device("sw1")

    def test_create_str_url_color_defaults(self):
        c = STPConfig.objects.create(device=self.device)
        self.assertEqual(str(c), f"STP: {self.device}")
        self.assertIn("/plugins/data-link/stp-configs/", c.get_absolute_url())
        self.assertEqual(c.mode, STPModeChoices.RSTP)
        self.assertEqual(c.get_mode_color(), "green")
        self.assertTrue(c.enabled)
        self.assertEqual(c.priority, 32768)

    def test_one_config_per_device(self):
        STPConfig.objects.create(device=self.device)
        with self.assertRaises(IntegrityError), transaction.atomic():
            STPConfig.objects.create(device=self.device, mode=STPModeChoices.MSTP)

    def test_cascade_from_device(self):
        c = STPConfig.objects.create(device=self.device)
        pk = c.pk
        self.device.delete()
        self.assertFalse(STPConfig.objects.filter(pk=pk).exists())


class STPInterfaceModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.device = create_test_device("sw1")
        cls.iface = _make_interface(cls.device, "ge-0/0/1")

    def test_create_str_url_defaults(self):
        si = STPInterface.objects.create(interface=self.iface, edge_port=True, bpdu_guard=True)
        self.assertEqual(str(si), f"STP: {self.iface}")
        self.assertIn("/plugins/data-link/stp-interfaces/", si.get_absolute_url())
        self.assertTrue(si.edge_port)
        self.assertTrue(si.bpdu_guard)
        self.assertFalse(si.root_guard)
        self.assertIsNone(si.priority)

    def test_one_override_per_interface(self):
        STPInterface.objects.create(interface=self.iface)
        with self.assertRaises(IntegrityError), transaction.atomic():
            STPInterface.objects.create(interface=self.iface, edge_port=True)

    def test_distinct_interfaces_allowed(self):
        other = _make_interface(self.device, "ge-0/0/2")
        STPInterface.objects.create(interface=self.iface, edge_port=True)
        si2 = STPInterface.objects.create(interface=other, root_guard=True)
        self.assertTrue(si2.root_guard)

    def test_cascade_from_interface(self):
        si = STPInterface.objects.create(interface=self.iface)
        pk = si.pk
        self.iface.delete()
        self.assertFalse(STPInterface.objects.filter(pk=pk).exists())


class LLDPConfigModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.device = create_test_device("sw1")

    def test_create_str_url_color_defaults(self):
        c = LLDPConfig.objects.create(device=self.device)
        self.assertEqual(str(c), f"LLDP: {self.device}")
        self.assertIn("/plugins/data-link/lldp-configs/", c.get_absolute_url())
        self.assertEqual(c.admin_status, LLDPAdminStatusChoices.ENABLED)
        self.assertEqual(c.get_admin_status_color(), "green")
        self.assertEqual(c.transmit_interval, 30)
        self.assertEqual(c.hold_multiplier, 4)

    def test_one_config_per_device(self):
        LLDPConfig.objects.create(device=self.device)
        with self.assertRaises(IntegrityError), transaction.atomic():
            LLDPConfig.objects.create(
                device=self.device, admin_status=LLDPAdminStatusChoices.TX_ONLY
            )


class LLDPInterfaceModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.device = create_test_device("sw1")
        cls.iface = _make_interface(cls.device, "ge-0/0/1")

    def test_create_str_url_color(self):
        li = LLDPInterface.objects.create(
            interface=self.iface, admin_status=LLDPAdminStatusChoices.TX_ONLY
        )
        self.assertEqual(str(li), f"LLDP: {self.iface}")
        self.assertIn("/plugins/data-link/lldp-interfaces/", li.get_absolute_url())
        self.assertEqual(li.get_admin_status_color(), "orange")

    def test_one_override_per_interface(self):
        LLDPInterface.objects.create(
            interface=self.iface, admin_status=LLDPAdminStatusChoices.RX_ONLY
        )
        with self.assertRaises(IntegrityError), transaction.atomic():
            LLDPInterface.objects.create(
                interface=self.iface, admin_status=LLDPAdminStatusChoices.DISABLED
            )


class DHCPSnoopingConfigModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.device = create_test_device("sw1")

    def test_create_str_url_defaults(self):
        c = DHCPSnoopingConfig.objects.create(device=self.device)
        self.assertEqual(str(c), f"DHCP snooping: {self.device}")
        self.assertIn("/plugins/data-link/dhcp-snooping-configs/", c.get_absolute_url())
        self.assertFalse(c.enabled)

    def test_vlans_array_roundtrip(self):
        c = DHCPSnoopingConfig.objects.create(device=self.device, enabled=True, vlans=[10, 20, 30])
        c.refresh_from_db()
        self.assertEqual(c.vlans, [10, 20, 30])

    def test_one_config_per_device(self):
        DHCPSnoopingConfig.objects.create(device=self.device)
        with self.assertRaises(IntegrityError), transaction.atomic():
            DHCPSnoopingConfig.objects.create(device=self.device, enabled=True)


class DHCPSnoopingInterfaceModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.device = create_test_device("sw1")
        cls.iface = _make_interface(cls.device, "ge-0/0/1")

    def test_create_str_url_defaults(self):
        di = DHCPSnoopingInterface.objects.create(interface=self.iface, trusted=True)
        self.assertEqual(str(di), f"DHCP snooping: {self.iface}")
        self.assertIn("/plugins/data-link/dhcp-snooping-interfaces/", di.get_absolute_url())
        self.assertTrue(di.trusted)

    def test_one_override_per_interface(self):
        DHCPSnoopingInterface.objects.create(interface=self.iface)
        with self.assertRaises(IntegrityError), transaction.atomic():
            DHCPSnoopingInterface.objects.create(interface=self.iface, trusted=True)

    def test_cascade_from_interface(self):
        di = DHCPSnoopingInterface.objects.create(interface=self.iface, trusted=True)
        pk = di.pk
        self.iface.delete()
        self.assertFalse(DHCPSnoopingInterface.objects.filter(pk=pk).exists())
