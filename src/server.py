from bluetooth_server import BluetoothApp

app = BluetoothApp()


@app.register('/')
def is_alive():
    pass


@app.register('/add-attendees')
def register_attendees():
    pass


@app.register('/get-attendees')
def get_attendees():
    pass


@app.register('/report')
def receive_report():
    pass


@app.register('/save-event')
def save_current_event():
    pass
