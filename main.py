from src.wrappers import ScreenWrapper, NFCWrapper

screen = ScreenWrapper()
screen.setup()
nfc = NFCWrapper()
nfc.setup()

screen.write("Started")

uid = nfc.get_uid()

screen.write(uid if uid else "Found nothing")
