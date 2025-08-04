import asyncio
from .database import db

async def init_db():
    await db.connect()
    # Optionally, could run schema creation here if needed
    # e.g., with open('app/db/schema.sql') as f: ...

async def close_db():
    await db.disconnect()

# To be called in FastAPI 'startup' and 'shutdown' events
