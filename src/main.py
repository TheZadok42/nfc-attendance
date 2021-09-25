import httpx

from .wrappers import NFCWrapper, ScreenWrapper

# TODO: remove prints
DAL_BASE_URL = 'http://192.168.1.105:8001'


def wait_for_card(nfc: NFCWrapper):
    uid = nfc.get_uid()
    while uid is None:
        uid = nfc.get_uid()
    return uid


async def send_user_atendance(uid: str):
    async with httpx.AsyncClient(base_url=DAL_BASE_URL) as client:
        response = await client.post('/attendance', json=dict(uid=uid))
        response.raise_for_status()


async def user_wait_loop(nfc: NFCWrapper, screen: ScreenWrapper):
    while True:
        screen.write('Press Your Card')
        uid = wait_for_card(nfc)
        screen.write('Registering')
        await send_user_atendance(uid)
        screen.write('Successfully Registered Attendance')


async def main():
    screen = ScreenWrapper()
    nfc = NFCWrapper()

    print("Setting up")
    screen.setup()
    nfc.setup()

    print("Running")
    await user_wait_loop(nfc, screen)
