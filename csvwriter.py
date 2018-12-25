import csv

## Write

rows = [
	{'Name' : 'Millea', 'Lastname': 'Duski', 'Age' : 23},
	{'Name' : 'Sathosi', 'Lastname': 'Nakamoto', 'Age' : 33},
	{'Name' : 'Jhon', 'Lastname': 'Doe', 'Age' : 37},
]
with open('writeData.csv', 'a') as filecsv:
	fields = ['Name', 'Lastname', 'Age']
	writer = csv.DictWriter(filecsv, fieldnames = fields)

	writer.writeheader()
	writer.writerows(rows)



