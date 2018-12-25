import json

with open('member.txt', 'r') as filemember:
	data = json.load(filemember)

	for member in data["member"]:
		print("The name is :" + member["Name"] + " and the Age is : " + member["Name"])