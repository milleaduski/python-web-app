import json

data = {}
data["member"] = [
	{'Name' : 'Millea', 'Lastname': 'Duski', 'Age' : 23},
	{'Name' : 'Sathosi', 'Lastname': 'Nakamoto', 'Age' : 33},
	{'Name' : 'Jhon', 'Lastname': 'Doe', 'Age' : 37}
]

with open('member.txt', 'w') as filemember:
	json.dump(data, filemember)