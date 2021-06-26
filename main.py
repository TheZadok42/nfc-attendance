from src.wrappers import ScreenWrapper, NFCWrapper

screen = ScreenWrapper()
screen.setup()
nfc = NFCWrapper()
nfc.setup()

screen.write("Press the tag")

uid = None
while uid is None:
    uid = nfc.get_uid()

screen.write(uid if uid else "Found nothing")
