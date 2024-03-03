from typing import Union
from fastapi import FastAPI
from models import user_model, film_model, user_model


app = FastAPI()

# database connection start from here
models.Base.metadata.create_all(engine)


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}