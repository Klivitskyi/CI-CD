from fastapi import FastAPI, HTTPException
from typing import Dict
from .schemas import ItemCreate, Item

app = FastAPI(title="Simple FastAPI App")

# In-memory "database"
_db: Dict[int, Item] = {}
_next_id = 1


@app.get("/")
def read_root():
    return {"message": "Hello, world!"}


@app.post("/items/", response_model=Item)
def create_item(item: ItemCreate):
    """Create an item and return it with an id."""
    global _next_id
    obj = Item(id=_next_id, **item.dict())
    _db[_next_id] = obj
    _next_id += 1
    return obj


@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    item = _db.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
