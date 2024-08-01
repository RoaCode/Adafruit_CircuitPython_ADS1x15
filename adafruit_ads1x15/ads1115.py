# SPDX-FileCopyrightText: 2018 Carter Nelson for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`ads1115`
====================================================

CircuitPython driver for 1115 ADCs.

* Author(s): Carter Nelson
"""
import struct

try:
    from typing import Dict, List

    from typing_extensions import Literal
except ImportError:
    pass

# pylint: disable=unused-import
from .ads1x15 import ADS1x15, Mode

# Data sample rates
_ADS1115_CONFIG_DR = {
    8: 0x0000,
    16: 0x0020,
    32: 0x0040,
    64: 0x0060,
    128: 0x0080,
    250: 0x00A0,
    475: 0x00C0,
    860: 0x00E0,
}

# Pins
P0 = 0
"""Analog Pin 0"""
P1 = 1
"""Analog Pin 1"""
P2 = 2
"""Analog Pin 2"""
P3 = 3
"""Analog Pin 3"""


class ADS1115(ADS1x15):
    """Class for the ADS1115 16 bit ADC."""

    @property
    def bits(self) -> Literal[16]:
        """The ADC bit resolution."""
        return 16

    @property
    def rates(self) -> List[int]:
        """Possible data rate settings."""
        r = list(_ADS1115_CONFIG_DR.keys())
        r.sort()
        return r

    @property
    def rate_config(self) -> Dict[int, int]:
        """Rate configuration masks."""
        return _ADS1115_CONFIG_DR

    def _data_rate_default(self) -> Literal[128]:
        """Default data rate setting is 128 samples per second"""
        return 128

    def _comp_low_thres_default(self) -> Literal[0x8000]:
        """Value is 16-bit, 2's complement.
        Defaults to 0x8000 as 16-bit hex (-32768 16-bit decimal)."""
        return 0x8000

    def _comp_high_thres_default(self) -> Literal[0x7FFF]:
        """Value is 16-bit, 2's complement.
        Defaults to 0x7FFF as 16-bit hex (32767 16-bit decimal)."""
        return 0x7FFF

    def _conversion_value(self, raw_adc: int) -> int:
        value = struct.unpack(">h", raw_adc.to_bytes(2, "big"))[0]
        return value
