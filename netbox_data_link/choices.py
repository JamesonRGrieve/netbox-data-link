# SPDX-License-Identifier: AGPL-3.0-or-later
"""Choice sets for the data-link model. Values match the switch config tokens verbatim."""

from utilities.choices import ChoiceSet


class STPModeChoices(ChoiceSet):
    """Spanning-tree protocol variant running on the bridge."""

    STP = "stp"
    RSTP = "rstp"
    MSTP = "mstp"
    CHOICES = [
        (STP, "STP (802.1D)"),
        (RSTP, "RSTP (802.1w)", "green"),
        (MSTP, "MSTP (802.1s)", "blue"),
    ]


class LLDPAdminStatusChoices(ChoiceSet):
    """LLDP agent administrative status (per IEEE 802.1AB) — bridge-wide or per-port override."""

    ENABLED = "enabled"
    DISABLED = "disabled"
    TX_ONLY = "tx_only"
    RX_ONLY = "rx_only"
    CHOICES = [
        (ENABLED, "Enabled (tx + rx)", "green"),
        (DISABLED, "Disabled", "red"),
        (TX_ONLY, "Transmit only", "orange"),
        (RX_ONLY, "Receive only", "cyan"),
    ]
