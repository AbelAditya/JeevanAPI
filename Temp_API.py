from fastapi import FastAPI
from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests

client = MongoClient("mongodb+srv://abeladityaphilipose:KVbLdrJ09fXw5Clc@jeevan.mgty77k.mongodb.net/?retryWrites=true&w=majority")

db = client.get_database('Data')
col = db.get_collection('Medicines')
col2 = db.get_collection('Popular')

app = FastAPI()

def helper(data):
    return {"id":data["id"],}

@app.get("/")
def home():
    return "This is home"

@app.get("/search")
def search(name: str):
    data = col.find({"Name":{"$regex":f"^{name}"}})
    d=[]
    for i in data:
        i.pop("_id")
        d.append(i)

    return {"data":d}

@app.get("/popular")
def popular():
    data = col2.find()
    d= []
    for i in data:
        i.pop("_id")
        d.append(i)

    return {"data":d}

@app.get("/desc")
def desc(url: str):
    r = requests.get(url)
    soup = BeautifulSoup(r.content,'html.parser')

    x = str(soup.find("meta",{"property":"og:description"}))
    end = x.find(".")
    return {"desc":x[15:end]}

