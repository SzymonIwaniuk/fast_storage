from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel
import boto3
from botocore.exceptions import ClientError

app = FastAPI()
session = boto3.Session(profile_name="aws-szymon-v04")

# Create an S3 client using the session
s3 = session.client("s3")


class S3Object(BaseModel):
    value: dict


@app.post("/items/")
def create_item(bucket_name: str, key: str, content: S3Object) -> dict:
    json_bytes = content.model_dump_json().encode("utf-8")
    try:
        return s3.put_object(
            Body=json_bytes, Bucket=bucket_name, Key=key, ContentType="application/json"
        )
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Client error {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/items/")
def get_item(bucket_name: str, key: str) -> dict:
    try:
        response = s3.get_object(Bucket=bucket_name, Key=key)
        return response

    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            raise HTTPException(
                status_code=404,
                detail=f"Object doesn't exists, or you don't have access to it: {e}",
            )
        else:
            raise HTTPException(status_code=400, detail=f"Something went wrong: {e}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {e}")


@app.delete("/items/")
def delete_item(bucket_name: str, key: str) -> dict:
    try:
        s3.head_object(Bucket=bucket_name, Key=key)
        response = s3.delete_object(Bucket=bucket_name, Key=key)
        return response

    except ClientError as e:

        if e.response["Error"]["Code"] == "404":
            raise HTTPException(
                status_code=404,
                detail=f"Object doesn't exists, or you don't have permission to delete it: {e}"
            )
        else:
            raise HTTPException(status_code=400, detail=f"Something went wrong: {e}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {e}")




