import pymongo
import datetime

TEST_MODULE = "day_count"

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["inclear"]

if TEST_MODULE == "event":
    col = db["event"] # user view
    # event : user_id, video_details
    e = {"userIdent": "furcifer", "strIdent": "-DfX3_CO2bU", "intTimestamp": 1617826241445, "strTitle": "Why you don't need certainty to be influential", "intCount": 1}
    id_ = col.insert_one(e)

    print(id_)
elif TEST_MODULE == "users":
    col = db["users"] # user view
    # event : user_id, video_details
    e = {"userIdent": "furcifer", "index": 0}
    id_ = col.insert_one(e)

    print(id_)
elif TEST_MODULE == "users_test":
    col = db["users"] # user view
    # event : user_id, video_details
    q = {"userIdent": "furcifer"}
    qr = col.find_one(q)
    print(qr)

    q = {"userIdent": "furcifer2"}
    qr = col.find_one(q)
    print(qr)

    print(col.count_documents({}))
elif TEST_MODULE == "videos":
    col = db["videos"] # user view
    # event : user_id, video_details
    e = {"strIdent": "-DfX3_CO2bX", "index": 0, "intTimestamp": 1617826241445, "strTitle": "Why you don't need certainty to be influential", "intCount": 1}
    id_ = col.insert_one(e)

    print(id_)
elif TEST_MODULE == "day_count":
    col = db["videos"] # user view
    # event : user_id, video_details
    e = {"strIdent": "-DfX3_CO2bX", "index": 0, "intTimestamp": 1617826241445, "strTitle": "Why you don't need certainty to be influential", "intCount": 1}
    id_ = col.find({})
    
    date_mapper = {}
    vids = list(id_)

    for v in vids:
        dt = v['intTimestamp']
        date = datetime.datetime.fromtimestamp(dt / 1e3).date()
        # print(date)
        date_mapper[str(date)] = date_mapper.get(str(date), 0) + 1

    print(date_mapper)

