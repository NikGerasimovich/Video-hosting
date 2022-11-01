import shutil
from typing import List
from fastapi import APIRouter, UploadFile, File, Form, Request
from fastapi.responses import JSONResponse

from schemas import UploadVideo, User, GetVideo, Message

video_router = APIRouter()


@video_router.post('/')
async def root(title: str = Form(...), description: str = Form(...), file: UploadFile = File(...)):
    info = UploadVideo(title=title, description=description)
    with open(f'{file.filename}', 'wb') as cv:  # open and save file
        shutil.copyfileobj(file.file, cv)

    return {'file_name': file.filename, 'info': info}


@video_router.post('/img', status_code=201)
async def upload_image(files: List[UploadFile] = File(...)):
    for img in files:
        with open(f'{img.filename}', 'wb') as cv:  # open and save file
            shutil.copyfileobj(img.file, cv)

    return {'file_name': 'Good'}


@video_router.get('/video', response_model=GetVideo, responses={404: {'model': Message}})
async def get_video():
    user = {'id': 24, 'name': 'Nick'}
    video = {'title': 'Test', 'description': 'Description'}
    info = GetVideo(user=user, video=video)
    return JSONResponse(status_code=200, content=info.dict())

