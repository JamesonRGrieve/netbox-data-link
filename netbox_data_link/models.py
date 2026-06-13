# SPDX-License-Identifier: AGPL-3.0-or-later
"""Data-link (L2) control-plane models. Each feature is a per-device singleton config
(OneToOne to ``dcim.Device``) plus per-PORT override rows that FK to ``dcim.Interface``.
Every key is a real column, so a switch's STP / LLDP / DHCP-snooping config round-trips
with zero loss — replacing the unstructured ``config_context`` it used to live under."""

from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from netbox.models import NetBoxModel
from .choices import LLDPAdminStatusChoices, STPModeChoices


class STPConfig(NetBoxModel):
    """Bridge-wide spanning-tree config for one switch (1:1 with the ``dcim.Device``).
    Per-port edge/guard overrides live in the child ``STPInterface`` rows."""

    device = models.OneToOneField(
        "dcim.Device",
        on_delete=models.CASCADE,
        related_name="stp_config",
        help_text="The switch this spanning-tree config applies to.",
    )
    enabled = models.BooleanField(default=True, help_text="Spanning tree enabled on the bridge.")
    mode = models.CharField(max_length=8, choices=STPModeChoices, default=STPModeChoices.RSTP)
    priority = models.PositiveIntegerField(
        default=32768,
        validators=[MinValueValidator(0), MaxValueValidator(61440)],
        help_text="Bridge priority (0–61440, in steps of 4096). Lower wins the root election.",
    )

    class Meta:
        ordering = ["device"]
        verbose_name = "STP Config"

    def __str__(self):
        return f"STP: {self.device}"

    def get_absolute_url(self):
        return reverse("plugins:netbox_data_link:stpconfig", args=[self.pk])

    def get_mode_color(self):
        return STPModeChoices.colors.get(self.mode)


class STPInterface(NetBoxModel):
    """Per-port spanning-tree override on one switch port (1:1 with the ``dcim.Interface``).
    Carries the edge-port / BPDU-guard / root-guard flags and an optional per-port priority."""

    interface = models.OneToOneField(
        "dcim.Interface",
        on_delete=models.CASCADE,
        related_name="stp_interface",
        help_text="The switch port this spanning-tree override applies to.",
    )
    priority = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(240)],
        help_text="Per-port priority (0–240, in steps of 16). Null = bridge default.",
    )
    edge_port = models.BooleanField(
        default=False, help_text="PortFast / edge port — skips listening/learning for end hosts."
    )
    bpdu_guard = models.BooleanField(
        default=False,
        help_text="Err-disable the port if a BPDU is received (edge-port protection).",
    )
    root_guard = models.BooleanField(
        default=False, help_text="Prevent the port from becoming a root port (topology protection)."
    )

    class Meta:
        ordering = ["interface"]
        verbose_name = "STP Interface"

    def __str__(self):
        return f"STP: {self.interface}"

    def get_absolute_url(self):
        return reverse("plugins:netbox_data_link:stpinterface", args=[self.pk])


class LLDPConfig(NetBoxModel):
    """Bridge-wide LLDP agent config for one switch (1:1 with the ``dcim.Device``).
    Per-port admin-status overrides live in the child ``LLDPInterface`` rows."""

    device = models.OneToOneField(
        "dcim.Device",
        on_delete=models.CASCADE,
        related_name="lldp_config",
        help_text="The switch this LLDP config applies to.",
    )
    admin_status = models.CharField(
        max_length=8, choices=LLDPAdminStatusChoices, default=LLDPAdminStatusChoices.ENABLED
    )
    transmit_interval = models.PositiveIntegerField(
        default=30,
        validators=[MinValueValidator(1)],
        help_text="Seconds between LLDP frame transmissions (msgTxInterval).",
    )
    hold_multiplier = models.PositiveIntegerField(
        default=4,
        validators=[MinValueValidator(1)],
        help_text="TTL multiplier (msgTxHold); advertised TTL = transmit_interval × hold_multiplier.",
    )

    class Meta:
        ordering = ["device"]
        verbose_name = "LLDP Config"

    def __str__(self):
        return f"LLDP: {self.device}"

    def get_absolute_url(self):
        return reverse("plugins:netbox_data_link:lldpconfig", args=[self.pk])

    def get_admin_status_color(self):
        return LLDPAdminStatusChoices.colors.get(self.admin_status)


class LLDPInterface(NetBoxModel):
    """Per-port LLDP admin-status override on one switch port (1:1 with the ``dcim.Interface``)."""

    interface = models.OneToOneField(
        "dcim.Interface",
        on_delete=models.CASCADE,
        related_name="lldp_interface",
        help_text="The switch port this LLDP override applies to.",
    )
    admin_status = models.CharField(
        max_length=8,
        choices=LLDPAdminStatusChoices,
        help_text="Per-port LLDP agent status, overriding the bridge default.",
    )

    class Meta:
        ordering = ["interface"]
        verbose_name = "LLDP Interface"

    def __str__(self):
        return f"LLDP: {self.interface}"

    def get_absolute_url(self):
        return reverse("plugins:netbox_data_link:lldpinterface", args=[self.pk])

    def get_admin_status_color(self):
        return LLDPAdminStatusChoices.colors.get(self.admin_status)


class DHCPSnoopingConfig(NetBoxModel):
    """Bridge-wide DHCP-snooping config for one switch (1:1 with the ``dcim.Device``).
    Per-port trust overrides live in the child ``DHCPSnoopingInterface`` rows."""

    device = models.OneToOneField(
        "dcim.Device",
        on_delete=models.CASCADE,
        related_name="dhcp_snooping_config",
        help_text="The switch this DHCP-snooping config applies to.",
    )
    enabled = models.BooleanField(default=False, help_text="DHCP snooping enabled on the bridge.")
    vlans = ArrayField(
        models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(4094)]),
        blank=True,
        null=True,
        help_text="VLAN IDs (1–4094) DHCP snooping is enabled on. Blank = none.",
    )

    class Meta:
        ordering = ["device"]
        verbose_name = "DHCP Snooping Config"

    def __str__(self):
        return f"DHCP snooping: {self.device}"

    def get_absolute_url(self):
        return reverse("plugins:netbox_data_link:dhcpsnoopingconfig", args=[self.pk])


class DHCPSnoopingInterface(NetBoxModel):
    """Per-port DHCP-snooping trust state on one switch port (1:1 with the ``dcim.Interface``).
    A trusted port is an uplink toward the legitimate DHCP server; untrusted ports drop
    server-sourced DHCP responses."""

    interface = models.OneToOneField(
        "dcim.Interface",
        on_delete=models.CASCADE,
        related_name="dhcp_snooping_interface",
        help_text="The switch port this DHCP-snooping trust state applies to.",
    )
    trusted = models.BooleanField(
        default=False,
        help_text="Trust DHCP server responses on this port (uplink toward the server).",
    )

    class Meta:
        ordering = ["interface"]
        verbose_name = "DHCP Snooping Interface"

    def __str__(self):
        return f"DHCP snooping: {self.interface}"

    def get_absolute_url(self):
        return reverse("plugins:netbox_data_link:dhcpsnoopinginterface", args=[self.pk])
