from fastapi import FastAPI, Form, Request, Path
from flask import request, jsonify
from pygments.lexers import templates
from pymongo import MongoClient
from pymongo import errors
import traceback
import pymongo
from starlette.responses import JSONResponse
import schema
from util import *
from fastapi.encoders import jsonable_encoder
import requests
from typing import Optional
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import json


app = FastAPI()



@app.get('/')
async def receiveLocationInfo(request: Request):
    print("OK")

    # result = await request.body()
    # result2 = result.decode('utf-8').split('&')
    # latitude = float(result2[0].split('=')[1])
    # longitude = float(result2[1].split('=')[1])
    #
    #
    # result3 = findLocation(latitude, longitude)
    #
    # if len(result3) == 0:
    #     return {"result": 1}
    #
    # print(result3[0])


    return {"success":1}
