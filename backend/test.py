import requests
BASE = "http://127.0.0.1:8000/"

response = requests.get(BASE+"/gettoken")
rjson=response.json()
inrix_token = rjson['result']['token']

#Testnearby
response = requests.get(BASE+"/getnearbyinfo",headers={'lat': '37.754647', 'long':'-122.429425'})
print(response.json())

#TestParking
# response = requests.get(BASE+"/getparking",headers={'Authorization': inrix_token, 'lat':'37.765199','long':'-122.417539'})
# parkR = response.json()
# parking_lots_info = []
# for parking_lot in parkR["result"]:
#     parking_lot_info = {
#         "type":'parking',
#         "name": parking_lot["name"],
#         "location": list(reversed(parking_lot["point"]["coordinates"]))
#     }
#     parking_lots_info.append(parking_lot_info)
# #Convert the list of dictionaries to a JSON object
# result_json = {"parking_lots": parking_lots_info}
# #Print or use the result_json as needed
# print(parkR)