import binascii
from typing import Optional

import RPi.GPIO as GPIO
from libs.nfc import PN532_SPI


class NFCWrapper:
    def __init__(self):
        self._connector = None

    def setup(self):
        self._connector = PN532_SPI(4, reset=20)
        self._connector.SAM_configuration()

    def get_uid(self, timeout: int = 100) -> Optional[str]:
        uid = self._connector.read_passive_target(timeout=timeout)
        return binascii.hexlify(uid).decode("utf-8") if uid else None

    def __del__(self):
        GPIO.cleanup()
