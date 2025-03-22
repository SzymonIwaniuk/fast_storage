from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()


# @app.post("/items/")
# async def create_item(bucket_id: int, item: dict):
#     """
#
#     Put this into Redis
#     Put this into s3
#     :param item:
#     :return:
#     """
#     return item

Objects = dict[str, dict]

buckets: dict[int, Objects] = {
    0: dict([
        ("test.txt", {1: 2})
    ]),
    1: dict([
        ("margonem.txt", {"weed": 420})
    ])
}

@app.get("/items/")
async def get_item(bucket_id: int, name: str) -> Objects:
    if bucket_id not in buckets:
        raise HTTPException(status_code=404, detail="Bucket not found")
    return buckets[bucket_id]