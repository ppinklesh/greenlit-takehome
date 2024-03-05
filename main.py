from typing import Union
from fastapi import FastAPI
from models.db_connection import get_db
from router import all_routers


app = FastAPI()
get_db()

app.include_router(all_routers.user_router)
app.include_router(all_routers.user_router)
app.include_router(all_routers.user_router)

@app.get('/')
async def home():
    return 'Welcome to Greenlit!'