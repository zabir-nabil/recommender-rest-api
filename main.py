from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel

from flurs.recommender import MFRecommender
from flurs.data.entity import User, Item, Event
import numpy as np

import uvicorn
import pymongo

threshold = 0.75

app = FastAPI()
app.recommender = MFRecommender(k=40) # attaching recommender to the fastapi server
app.recommender.initialize()

app.client = pymongo.MongoClient("mongodb://localhost:27017/")
app.db = app.client["inclear"]
# each time the server restarts it needs to insert all the events to the recommender
# register all users
for u in app.db["users"].find({}):
    app.recommender.register(User(u["index"]))
for v in app.db["videos"].find({}):
    app.recommender.register(Item(v["index"]))

class Video(BaseModel):
    strIdent: str
    strTitle: str
    intTimestamp: int
    intCount: int


class UserH(BaseModel):
    userIdent: str
    userHistory: List[Video] = []
    is_new: Optional[bool] = None


@app.get("/")
def read_root():
    return {"msg": "The server is live!", "success": 1}

# route for getting recomendation just from an user id without any additional data
# returns a list of video 
@app.get("/video_recommendation/users/{user_id}")
def user_recom(user_id: str, is_new: Optional[bool] = None):
    # only user id
    # check if it exits
    q = {"userIdent": user_id}
    qr = app.db["users"].find_one(q)

    if qr == None: # completely new user
        return {"video_list": [], "msg": "the user is not registered in the system"}
    else: # the user is registered
        user_idx = User(qr["index"])
        n_vids = app.db["videos"].count_documents({})
        potential_video_indices = np.array(range(n_vids)) # initially select all videos
        vids, vscores = app.recommender.recommend(user_idx, potential_video_indices)
        vidents = []

        for vi, vs in zip(vids, vscores):
            if vs > threshold:
                print(vs)
                q = {"index": int(vi)}
                qr = app.db["videos"].find_one(q)
                try:
                    vidents.append(qr["strIdent"])
                except:
                    print("some internal database error")
        return {"video_strIndents": vidents, "msg": "success"}



    return {"user_id": user_id, "is_new": is_new}

# route for getting recomendation just from an user id with additional video data
# returns a list of video in User object
@app.post("/video_recommendation/users/")
def user_recom_with_data(user: UserH):
    # register all the events
    # check if it exits
    q = {"userIdent": user.userIdent}
    qr = app.db["users"].find_one(q)
    if qr == None: # completely new user
        # register to database
        idx_ = app.db["users"].count_documents({})
        e = {"userIdent": user.userIdent, "index": idx_}
        app.db["users"].insert_one(e)
        # register to recom
        user_c = User(idx_)
        app.recommender.register(user_c)
    else:
        user_c = User(int(qr["index"]))
    # register all videos
    for v in user.userHistory:
        q = {"strIdent": v.strIdent}
        qr = app.db["videos"].find_one(q)
        if qr == None:
            # new video
            idx_ = app.db["videos"].count_documents({}) 
            e = {"strIdent": v.strIdent, "index": idx_, "intTimestamp": v.intTimestamp, "strTitle": v.strTitle, "intCount": v.intCount}
            app.db["videos"].insert_one(e)
            # register to recom
            video_c = Item(idx_)
            app.recommender.register(video_c)
        else:
            video_c = Item(qr["index"])

        # record event
        event = Event(user_c, video_c)
        app.recommender.update(event)

    return {"user_id": user.userIdent, "msg": "recommender updated"}

# route for getting recomendation just from a video
# returns a list of video in User object (the strIndent being "NOT_REGISTERED")
@app.post("/video_recommendation/videos/")
def video_recom_with_data(video: Video):
    return {"video_id": video.strIdent, "video_title": video.strTitle}


if __name__ == '__main__':
    uvicorn.run(app, port=80, host='0.0.0.0')