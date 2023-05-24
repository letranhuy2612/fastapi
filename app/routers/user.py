from io import BytesIO
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile,status, Path

from app.minio_handler import MinioHandler
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from starlette.responses import StreamingResponse

router = APIRouter()


@router.get('/me', response_model=schemas.UserResponse)
def get_me(db: Session = Depends(get_db), user_id: str = Depends(oauth2.require_user)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return user

@router.post("/upload/minio", response_model=schemas.UploadFileResponse)
async def upload_file_to_minio(file: UploadFile, db: Session = Depends(get_db), user_id: str = Depends(oauth2.require_user)):
    try:
        data = file.file.read()

        file_name = " ".join(file.filename.strip().split())

        data_file = MinioHandler().get_instance().put_object(
            file_name=file_name,
            file_data=BytesIO(data),
            content_type=file.content_type
        )
        return data_file
    except Exception as e:
        error = e.__class__.__name__
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)

@router.get("/download/minio/{filePath}")
def download_file_from_minio(
        *, filePath: str = Path(..., title="The relative path to the file", min_length=1, max_length=500)):
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