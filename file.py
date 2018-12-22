## Open file

# file = open('example.txt', 'r+')

# file.write('The system is writing in the file example.txt write and read')
# result = file.read()

# print(result)

# file = open('example.txt', 'a+')

# file.write('\n This is an additional word')
# file.seek(0)
# result = file.read()

# print(result)

file = open('example.txt', 'a+')

def addList(text):
	file.write('\n' + text)
	dataInput()

def dataInput():
	addList(input('What Your list ?'))


dataInput()