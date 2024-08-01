# SPDX-FileCopyrightText: 2018 Carter Nelson for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`ads1015`
====================================================

CircuitPython driver for ADS1015 ADCs.

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
_ADS1015_CONFIG_DR = {
    128: 0x0000,
    250: 0x0020,
    490: 0x0040,
    920: 0x0060,
    1600: 0x0080,
    2400: 0x00A0,
    3300: 0x00C0,
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


class ADS1015(ADS1x15):
    """Class for the ADS1015 12 bit ADC."""

    @property
    def bits(self) -> Literal[12]:
        """The ADC bit resolution."""
        return 12

    @property
    def rates(self) -> List[int]:
        """Possible data rate settings."""
        r = list(_ADS1015_CONFIG_DR.keys())
        r.sort()
        return r

    @property
    def rate_config(self) -> Dict[int, int]:
        """Rate configuration masks."""
        return _ADS1015_CONFIG_DR

    def _data_rate_default(self) -> Literal[1600]:
        """Default data rate setting is 1600 samples per second"""
        return 1600

    def _comp_low_thres_default(self) -> Literal[0x8000]:
        """Value is 12-bit, 2's complement stored in 16-bit register where 4 LSBs are 0.
        Defaults to 0x8000 as 16-bit hex (-2048 as 12-bit decimal)."""
        return 0x8000

    def _comp_high_thres_default(self) -> Literal[0x7FF0]:
        """Value is 12-bit, 2's complement stored in 16-bit register where 4 LSBs are 0.
        Defaults to 0x7FF0 as 16-bit hex (2047 as 12-bit decimal)."""
        return 0x7FF0

    def _conversion_value(self, raw_adc: int) -> int:
        value = struct.unpack(">h", raw_adc.to_bytes(2, "big"))[0]
        return value
