from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import shutil
import os
import schemas, crud, models, database, auth

router = APIRouter()

UPLOAD_DIRECTORY = "./uploaded_files"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

@router.post("/uploadfile/", response_model=schemas.File)
async def upload_file(file: UploadFile = File(...), current_user: models.User = Depends(auth.get_current_active_user), db: Session = Depends(database.get_db)):
    if file.content_type not in ["application/pdf", "image/png", "image/jpeg", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    db_file = schemas.FileCreate(filename=file.filename, file_type=file.content_type)
    return crud.create_file(db=db, file=db_file, owner_id=current_user.id)

@router.get("/files/", response_model=List[schemas.File])
async def list_files(current_user: models.User = Depends(auth.get_current_active_user), db: Session = Depends(database.get_db)):
    return crud.get_files(db=db, owner_id=current_user.id)

# @router.get("/files/{filename}", response_class=FileResponse)
# async def get_file(filename: str, current_user: models.User = Depends(auth.get_current_active_user)):
#     file_path = os.path.join(UPLOAD_DIRECTORY, filename)
#     if not os.path.exists(file_path):
#         raise HTTPException(status_code=404, detail="File not found")
#     return file_path

@router.delete("/files/{filename}")
async def delete_file(filename: str, current_user: models.User = Depends(auth.get_current_active_user), db: Session = Depends(database.get_db)):
    file_path = os.path.join(UPLOAD_DIRECTORY, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    os.remove(file_path)
    file = db.query(models.File).filter(models.File.filename == filename).first()
    if file:
        crud.delete_file(db=db, file_id=file.id)
    return {"detail": "File deleted successfully"}
