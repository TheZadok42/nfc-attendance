from fastapi import FastAPI

from src.dal.tables import engine, metadata

from .routes import attendance_router, attendees_router, events_router

app = FastAPI(title='Attendance Backend', version='0.0.1')

app.include_router(events_router)
app.include_router(attendees_router)
app.include_router(attendance_router)


@app.get('/')
async def is_alive():
    pass


@app.on_event('startup')
async def on_start_up():
    metadata.create_all(engine)
