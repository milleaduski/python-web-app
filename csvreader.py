import csv

data = []

with open('data.csv', 'r') as filecsv:
	csvreader = csv.reader(filecsv)
	for row in csvreader:
		data.append(row)
	print('Total row : ', csvreader.line_num)
print(data)