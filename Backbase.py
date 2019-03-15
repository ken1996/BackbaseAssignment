import csv
import datetime
import sys
#start at 0
#overdraft unlimited on current acc
#savings can not drop below 0
#feature automatically transfers funds from savings if current account drops below 0



#ISO-8601 datetime. Z means microseconds?
def dateTimeISO():
	fullDate=str(datetime.datetime.now().isoformat()).split()
	time= fullDate[0].split(".")
	returnString = time[0] +"Z"
	return returnString

def checkSavings ():
	totalSavings= 0
	for value in savingsDict:
		totalSavings +=savingsDict[value]["Balance"] 
	return totalSavings

def createCurrent(row):
	currentDict[row[0]]={}
	currentDict[row[0]]["Balance"] =float(row[4]) 

def addToCurrent(row):
	addition = float(row[4])
	currentBalance = currentDict[row[0]]["Balance"]
	newBalance = addition + currentBalance
	if newBalance > 0:
		currentDict[row[0]]["Balance"] = newBalance
	else:
		takeFromSavings(row,newBalance)

	
#once we see an input that would take too much from current account
#need to first take away from savigns account and add to current


def createSavings(row):
	savingsDict[row[0]]={}
	savingsDict[row[0]]["Balance"] =float(row[4]) 

def addToSavings(row):
	savingsDict[row[0]]["Balance"] += float(row[4]) 

#assume that user has multiple savings accounts and can pay it off via his combined savings. 
#takes from until savings account hits £0
#if no money in savings account then current account goes into negative
def takeFromSavings(row,newBalance):
	for value in savingsDict:
		chipBalance = newBalance + savingsDict[value]["Balance"]
		if  chipBalance >= 0:
			#take money from Savings
			lines2.append(addTransaction("takeSavings",value,newBalance))
			#add money to Current
			lines2.append(addTransaction("addCurrent",row[0], newBalance))
			#turn current balance for Current Account to £0 
			currentDict[row[0]]["Balance"] = 0
		else:
			#takes all money from savings + adds amount to current account
			#then makes the current account balance the difference from savings and transaction 
			new = savingsDict[value]["Balance"]
			lines2.append(addTransaction("takeSavings",value,-savingsDict[value]["Balance"]))
			lines2.append(addTransaction("addCurrent",row[0], -new))
			currentDict[row[0]]["Balance"] = chipBalance

	#print(savings_Balance)

# take from savings + add to Current Account transaction
#uses ISO time
def addTransaction(type, value,balance):
	if type == "takeSavings":
		time= dateTimeISO()
		savingsDict[value]["Balance"] += balance
		returnString = [value,  "SAVINGS", "SYSTEM", time ,balance]
		return returnString
	if type == "addCurrent":
		time= dateTimeISO()
		print(balance)
		currentDict[row[0]]["Balance"] -= balance
		returnString = [value,  "CURRENT", "SYSTEM" , time, -balance]
		return returnString


# creates dictionaries which act as the current account and savings account.
currentDict = {}
savingsDict = {}

#lines stores the input ledger into a list
#lines2 stores the updated ledger
lines= []
lines2 =[]
#reads csv file in cmd line. e.g  program.py  file.csv
file_name = sys.argv[1]
#opens field and copies contents into list "lines"
with open(file_name, "r") as readFile:
	reader = csv.reader(readFile)
	lines = list(reader)


#iterates through lines, appends to current and savings account dictionaries
#appends transactions to lines2
#if new transactions happen it goes through addTo functions and writes transactions.
#if current account transactions cause current account to go into overdraft, use takeFromSavings() function
#to take money from savings automatically from system. 
for row in lines:
	if row[1] =="CURRENT" and row[0] in currentDict:
		addToCurrent(row)
	if row[1] =="SAVINGS" and row[0] in savingsDict:
		addToSavings(row)
	if row[1] =="CURRENT" and row[0] not in currentDict:
		createCurrent(row)
	if row[1] =="SAVINGS" and row[0] not in savingsDict:
		createSavings(row)
	lines2.append(row)

#with open("customer-1234567-ledger.csv", "r") as writeFile:		
#writes a csv file with update transactions
with open('result.csv', 'w',newline='') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerows(lines2)

readFile.close()
writeFile.close()




#prints the current dictionary states
#print(currentDict)
#print(savingsDict)

