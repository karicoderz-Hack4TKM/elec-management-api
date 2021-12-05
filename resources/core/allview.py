import pymongo
import numpy as np

connect = pymongo.MongoClient("mongodb+srv://1012hackathon:1012tkmce@cluster0.9tsp4.mongodb.net")
selectDb = connect["hackthon"]
selectCollection = selectDb["users"]
agg_result = selectCollection.aggregate(
    [{
        "$group":
            {"_id": "$usertype",
             "count": {"$sum": 1}
             }}
    ])

data = [x for x in agg_result]
for i in range(len(data)):
    doc = selectCollection.find_one({"usertype":data[i]["_id"]})
    value = np.array(doc['12']).mean()
    data[i]["average"]=value
# print(data)
