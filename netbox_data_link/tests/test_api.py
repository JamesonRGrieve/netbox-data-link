# SPDX-License-Identifier: AGPL-3.0-or-later
"""REST API CRUD tests against a real DB + real API client (no mocks).

Composes the explicit CRUD mixins (not the GraphQL-inclusive APIViewTestCase) since the
plugin ships no GraphQL type yet. Each per-device singleton is OneToOne to dcim.Device and
each per-port override is OneToOne to dcim.Interface, so every created object needs a fresh
device/interface."""

from dcim.models import Interface
from utilities.testing import APIViewTestCases, create_test_device
from netbox_data_link.models import (
    DHCPSnoopingConfig,
    DHCPSnoopingInterface,
    LLDPConfig,
    LLDPInterface,
    STPConfig,
    STPInterface,
)


class _CRUD(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
):
    pass


def _devices(prefix, count):
    return [create_test_device(f"{prefix}{i}") for i in range(count)]


def _interfaces(device, prefix, count):
    return [
        Interface.objects.create(device=device, name=f"{prefix}{i}", type="1000base-t")
        for i in range(count)
    ]


class STPConfigAPITest(_CRUD):
    model = STPConfig
    brief_fields = ["device", "display", "id", "mode", "url"]
    bulk_update_data = {"priority": 4096}

    @classmethod
    def setUpTestData(cls):
        existing = _devices("STPC-EX", 3)
        STPConfig.objects.bulk_create([STPConfig(device=d) for d in existing])
        fresh = _devices("STPC-NEW", 3)
        cls.create_data = [
            {"device": fresh[0].pk, "enabled": True, "mode": "rstp", "priority": 32768},
            {"device": fresh[1].pk, "enabled": False, "mode": "stp", "priority": 0},
            {"device": fresh[2].pk, "enabled": True, "mode": "mstp", "priority": 8192},
        ]


class STPInterfaceAPITest(_CRUD):
    model = STPInterface
    brief_fields = ["display", "id", "interface", "url"]
    bulk_update_data = {"bpdu_guard": True}

    @classmethod
    def setUpTestData(cls):
        device = create_test_device("STPI-SW")
        existing = _interfaces(device, "ex", 3)
        STPInterface.objects.bulk_create([STPInterface(interface=i) for i in existing])
        fresh = _interfaces(device, "new", 3)
        cls.create_data = [
            {"interface": fresh[0].pk, "edge_port": True, "bpdu_guard": True},
            {"interface": fresh[1].pk, "priority": 16, "root_guard": True},
            {"interface": fresh[2].pk, "edge_port": False},
        ]


class LLDPConfigAPITest(_CRUD):
    model = LLDPConfig
    brief_fields = ["admin_status", "device", "display", "id", "url"]
    bulk_update_data = {"transmit_interval": 60}

    @classmethod
    def setUpTestData(cls):
        existing = _devices("LLDPC-EX", 3)
        LLDPConfig.objects.bulk_create([LLDPConfig(device=d) for d in existing])
        fresh = _devices("LLDPC-NEW", 3)
        cls.create_data = [
            {
                "device": fresh[0].pk,
                "admin_status": "enabled",
                "transmit_interval": 30,
                "hold_multiplier": 4,
            },
            {
                "device": fresh[1].pk,
                "admin_status": "tx_only",
                "transmit_interval": 15,
                "hold_multiplier": 3,
            },
            {"device": fresh[2].pk, "admin_status": "disabled"},
        ]


class LLDPInterfaceAPITest(_CRUD):
    model = LLDPInterface
    brief_fields = ["admin_status", "display", "id", "interface", "url"]
    bulk_update_data = {"admin_status": "rx_only"}

    @classmethod
    def setUpTestData(cls):
        device = create_test_device("LLDPI-SW")
        existing = _interfaces(device, "ex", 3)
        LLDPInterface.objects.bulk_create(
            [LLDPInterface(interface=i, admin_status="enabled") for i in existing]
        )
        fresh = _interfaces(device, "new", 3)
        cls.create_data = [
            {"interface": fresh[0].pk, "admin_status": "tx_only"},
            {"interface": fresh[1].pk, "admin_status": "rx_only"},
            {"interface": fresh[2].pk, "admin_status": "disabled"},
        ]


class DHCPSnoopingConfigAPITest(_CRUD):
    model = DHCPSnoopingConfig
    brief_fields = ["device", "display", "id", "url"]
    bulk_update_data = {"enabled": True}

    @classmethod
    def setUpTestData(cls):
        existing = _devices("DHCPC-EX", 3)
        DHCPSnoopingConfig.objects.bulk_create([DHCPSnoopingConfig(device=d) for d in existing])
        fresh = _devices("DHCPC-NEW", 3)
        cls.create_data = [
            {"device": fresh[0].pk, "enabled": True, "vlans": [10, 20, 30]},
            {"device": fresh[1].pk, "enabled": False},
            {"device": fresh[2].pk, "enabled": True, "vlans": [100]},
        ]


class DHCPSnoopingInterfaceAPITest(_CRUD):
    model = DHCPSnoopingInterface
    brief_fields = ["display", "id", "interface", "trusted", "url"]
    bulk_update_data = {"trusted": True}

    @classmethod
    def setUpTestData(cls):
        device = create_test_device("DHCPI-SW")
        existing = _interfaces(device, "ex", 3)
        DHCPSnoopingInterface.objects.bulk_create(
            [DHCPSnoopingInterface(interface=i) for i in existing]
        )
        fresh = _interfaces(device, "new", 3)
        cls.create_data = [
            {"interface": fresh[0].pk, "trusted": True},
            {"interface": fresh[1].pk, "trusted": False},
            {"interface": fresh[2].pk, "trusted": True},
        ]
