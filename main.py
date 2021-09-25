from src.dal.tables import engine, metadata

# from src.wrappers import NFCWrapper, ScreenWrapper

metadata.create_all(engine)

# screen = ScreenWrapper()
# nfc = NFCWrapper()

# screen.setup()
# nfc.setup()

# screen.write("Press the tag")

# uid = None
# while uid is None:
#     uid = nfc.get_uid()

# screen.write(uid if uid else "Found nothing")
