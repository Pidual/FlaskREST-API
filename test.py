import requests

BASE = "http://127.0.0.1:5000/"

#data = [{"likes":66,"name":"Gangplank","views":700},
#        {"likes":23,"name":"Ryzen 7 vs Intel 12!","views":300},
#       {"likes":200,"name":"Tim is weird Expose video","views":5000},
#       {"likes":1600,"name":"Riot games is trash","views":80000},
#        {"likes":67000,"name":"Learning flask","views":600000}]

for i in range(6):
    response = requests.get(BASE+"video/"+str(i))
    print(response.json())

input()
response = requests.delete(BASE + "video/0")
print(response)

input()
response = requests.get(BASE + "video/2")
print(response.json())