from io import BytesIO
from fastapi import APIRouter, Body, Form, Depends, File, HTTPException, UploadFile,status, Path
from pydantic import BaseModel

from app.utils.minio_handler import MinioHandler
from ..utils import oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from .. import schemas
from app.models.models import Metadata, User
from starlette.responses import StreamingResponse

router = APIRouter()



@router.post("/upload/minio", response_model=schemas.UploadFileResponse)
async def upload_file_to_minio(metadata: schemas.MetadataBaseSchema = Body(...),file: UploadFile=File(...), db: Session = Depends(get_db), user_id: str = Depends(oauth2.require_user)):
    try:
        data = file.file.read()
        file_name = " ".join(file.filename.strip().split())
        data_file = MinioHandler().get_instance().put_object(
            file_name=file_name,
            file_data=BytesIO(data),
            content_type=file.content_type
        )
        metadata.bucket_name = data_file['bucket_name']
        metadata.file_path = data_file['file_name']
        metadata.owner_id = user_id
        new = Metadata(**metadata.dict())
        db.add(new)
        db.commit()
        return data_file
    except Exception as e:
        error = e.__class__.__name__
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)

@router.get("/download/minio/{filePath}")
def download_file_from_minio(
        *, filePath: str = Path(..., min_length=1, max_length=500)):
    try:
        minio_client = MinioHandler().get_instance()
        if not minio_client.check_file_name_exists(minio_client.bucket_name, filePath):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                  detail='File not exists')

        file = minio_client.client.get_object(minio_client.bucket_name, filePath).read()
        return StreamingResponse(BytesIO(file))
    except Exception as e:
        error = e.__class__.__name__
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)