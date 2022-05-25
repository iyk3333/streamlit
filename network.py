import traceback
import requests



class Payload:
    def __init__(self):
        self.locationInfo = {
            'latitude': None,
            'longitude': None,
        }

#
# def sendData(data: dict):
#     try:
#         url = "http://127.0.0.1:8000/locationInfoModel"
#         result = requests.post(url=url, json=data)
#
#         if result.status_code == 200:
#             print("state good")
#             return str(result[0].content.decode('utf-8'))
#         else:
#             print("state bad")
#
#     except:
#         print(traceback.format_exc())