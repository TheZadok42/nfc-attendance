import binascii

from libs.nfc import PN532_SPI


class NFCWrapper:
    def __init__(self):
        self._connector = None

    def setup(self):
        self._connector = PN532_SPI(4, reset=20)
        self._connector.SAM_configuration()

    def get_uid(self):
        uid = self._connector.read_passive_target()
        return binascii.hexlify(uid).decode("utf-8")
