from flask import Flask, render_template, request, redirect, url_for
from bson import ObjectId, json_util
import json
from pymongo import MongoClient
from flask_cors import CORS
import os

app = Flask(__name__)

CORS(app)

ENV = "dev"

if ENV == "dev":
    app.debug = True
    client = MongoClient(
        "mongodb+srv://admin:admin@cluster0.njsya.mongodb.net/bcg_project?retryWrites=true&w=majority")
else:
    app.debug = False
    client = MongoClient(
        "mongodb+srv://admin:admin@cluster0.njsya.mongodb.net/bcg_project?retryWrites=true&w=majority")

db = client.bcg_project
PolicyCollection = db.policies


@app.route("/", methods=["GET"])
def HomeTestRoute():
    return("Test Home")


@app.route("/api/get-all-policies", methods=["GET"])
def getAllPolicies():
    if(request.method == "GET"):
        allPolicies = list(PolicyCollection.find())

        if (allPolicies != None):
            jsonString = json.dumps(allPolicies, default=json_util.default)
            josnResponse = json.loads(jsonString)
            return {"status": 200,
                    "apiData": josnResponse,
                    "result": "success",
                    "message": "Fetched all data"}
        else:
            return {"status": 501,
                    "apiData": {},
                    "result": "fail",
                    "message": "Error in fetching data"}


@app.route("/api/update-user-policy", methods=["PATCH"])
def updateUserPolicy():
    if(request.method == "PATCH"):
        if(request.json["policy_id"] == None
                or request.json["date_of_purchase"] == None
                or request.json["customer_id"] == None
                or request.json["fuel"] == None
                or request.json["vechile_segment"] == None
                or request.json["premium"] == None
                or request.json["bodily_injury_liability"] == None
                or request.json["personal_injury_protection"] == None
                or request.json["property_damage_liability"] == None
                or request.json["collision"] == None
                or request.json["comprehensive"] == None
                or request.json["customer_gender"] == None
                or request.json["customer_income_group"] == None
                or request.json["customer_region"] == None
                or request.json["customer_marital_status"] == None):
            return {"status": 400,
                    "apiData": {},
                    "result": "fail",
                    "message": "Inviad Api Request"}
        else:
            singlePolicy = list(PolicyCollection.find(
                {"policy_id": request.json["policy_id"]}))

            if (singlePolicy != None):
                PolicyCollection.update({"policy_id": request.json["policy_id"]}, {"$set":
                                                                                   {"fuel": request.json["fuel"],
                                                                                    "vechile_segment": request.json["vechile_segment"],
                                                                                    "premium": request.json["premium"],
                                                                                    "bodily_injury_liability": request.json["bodily_injury_liability"],
                                                                                    "personal_injury_protection": request.json["personal_injury_protection"],
                                                                                    "property_damage_liability": request.json["property_damage_liability"],
                                                                                    "collision": request.json["collision"],
                                                                                    "comprehensive": request.json["comprehensive"],
                                                                                    "customer_gender": request.json["customer_gender"],
                                                                                    "customer_income_group": request.json["customer_income_group"],
                                                                                    "customer_region": request.json["customer_region"],
                                                                                    "customer_marital_status": request.json["customer_marital_status"]}})

                return {"status": 200,
                        "apiData": {},
                        "result": "success",
                        "message": "Policy Record Updated"}

            else:
                return {"status": 501,
                        "apiData": {},
                        "result": "fail",
                        "message": "No Record Found"}


if __name__ == "__main__":
    app.run()
