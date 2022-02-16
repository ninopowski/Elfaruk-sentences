"""
1. Registration of a user
2. User to store a sentence on our db for 1 token (has 10 tokens)
3. Retrieve a sentence from the db for 1 token
"""

import bcrypt
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

        # hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # store the username and password in the database
        users.insert_one(
            {
                "username": username,
                "password": hashed_password,
                "sentences": [],
                "tokens": 6
            }
        )
        retMap = {
            "status code": 200,
            "message": "You've successfully registered for the API"
        }
        return jsonify(retMap)


def verifyPw(username, password):
    hashed_pw = users.find({
        "username": username
    })[0]["password"]
    if bcrypt.checkpw(password.encode('utf-8'), hashed_pw):
        return True
    else:
        print(bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()))
        print(hashed_pw)
        return False


def countTokens(username):
    tokens = users.find({"username": username})[0]["tokens"]
    return int(tokens)


class Store(Resource):

    def post(self):
        # get posted data
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]
        sentence = postedData["sentence"]

        # verify username and password
        correct_pw = verifyPw(username, password)

        if not correct_pw:
            retMap = {
                "status code": 301,
                "message": "invalid username or password"
                }
            return jsonify(retMap)

        # verify user has enough tokens
        num_tokens = countTokens(username)
        if num_tokens <= 0:
            retMap = {
                "status code": 301,
                "message": "not enough tokens"
            }
            return jsonify(retMap)
        else:


        # store the sentence and return
            users.update_one({
                "username": username
            }, {
                "$set":{
                    "sentence": sentence,
                    "tokens": num_tokens-1}
            })

            retMap = {
                "status code": 200,
                "message": "save successful"
            }

            return jsonify(retMap)


class Retrieve(Resource):
    def post(self):
        # get posted data
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]

        connected = verifyPw(username, password)
        num_tokens = countTokens(username)

        if not connected:
            retMap = {
                "status code": 301,
                "message": "invalid username or password"
            }
            return jsonify(retMap)
        else:
            if num_tokens <= 0:
                retMap = {
                    "status code": 301,
                    "message": "not enough tokens"
                }
                return jsonify(retMap)
            else:
                user = users.find({"username": username})[0]
                retMap = {
                    "username": user["username"],
                    "sentence": user["sentences"]
                }
                users.update_one({"username": username}, {"$set":{"tokens": num_tokens -1}})
                return jsonify(retMap)


api.add_resource(Register, "/register")
api.add_resource(Store, "/store")
api.add_resource(Retrieve, "/retrieve")


if __name__ == "__main__":
    app.run(debug=True)