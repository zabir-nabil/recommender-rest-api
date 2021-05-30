from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel

import uvicorn

app = FastAPI()


class Video(BaseModel):
    strIdent: str
    strTitle: str
    intTimestamp: int
    intCount: int


class User(BaseModel):
    userIdent: str
    userHistory: List[Video] = []
    is_new: Optional[bool] = None


@app.get("/")
def read_root():
    return {"msg": "The server is live!", "success": 1}

# route for getting recomendation just from an user id without any additional data
# returns a list of video in User object
@app.get("/video_recommendation/users/{user_id}")
def user_recom(user_id: str, is_new: Optional[bool] = None):
    return {"user_id": user_id, "is_new": is_new}

# route for getting recomendation just from an user id with additional video data
# returns a list of video in User object
@app.post("/video_recommendation/users/")
def user_recom_with_data(user: User):
    return {"user_id": user.userIdent, "user_history": user.userHistory}

# route for getting recomendation just from a video
# returns a list of video in User object (the strIndent being "NOT_REGISTERED")
@app.post("/video_recommendation/videos/")
def video_recom_with_data(video: Video):
    return {"video_id": video.strIdent, "video_title": video.strTitle}


if __name__ == '__main__':
    uvicorn.run(app, port=80, host='0.0.0.0')