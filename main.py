"""
1. Registration of a user
2. User to store a sentence on our db for 1 token (has 10 tokens)
3. Retrieve a sentence from the db for 1 token
"""


from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from pymongo import MongoClient


app = Flask(__name__)
api = Api(app)

cluster = "mongodb+srv://nino:1234@cluster.p9rri.mongodb.net/test"
client = MongoClient(cluster)

db = client.SentencesDatabase

users = db.Users

class Register(Resource):

    def post(self):
        # get posted data from the user
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]






if __name__ == "__main__":
    app.run(debug=True)