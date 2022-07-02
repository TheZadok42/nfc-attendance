import time

import httpx

from .wrappers import NFCWrapper, ScreenWrapper

DAL_BASE_URL = 'https://nfc-attendance-achva.herokuapp.com/'


def wait_for_card(nfc: NFCWrapper):
    uid = nfc.get_uid()
    while uid is None:
        uid = nfc.get_uid()
    return uid


async def send_user_attendance(uid: str):
    async with httpx.AsyncClient(base_url=DAL_BASE_URL) as client:
        response = await client.post('/attendance/',
                                     params=dict(nfc_card_uid=uid))
        response.raise_for_status()


async def user_wait_loop(nfc: NFCWrapper, screen: ScreenWrapper):
    while True:
        screen.write('Press Your Card')
        uid = wait_for_card(nfc)
        screen.write('Registering')
        try:
            await send_user_attendance(uid)
        except httpx.HTTPStatusError as error:
            screen.write('Failed to Register Attendance')
            try:
                print(error.response.json())
            except:
                print(error.response.content)
        else:
            screen.write('Successfully Registered Attendance')
        time.sleep(1)


async def main():
    screen = ScreenWrapper()
    nfc = NFCWrapper()

    print("Setting up")
    screen.setup()
    nfc.setup()

    print("Running")
    await user_wait_loop(nfc, screen)
