from decimal import Decimal

#Method to find the first instance of a character and return its index
def findCharacter(string, char):
	for x in range(0, len(string)):
		if string[x] == char:
			return x
	return -1

#Method to find a full number directly before an index and return its String value
def numBefore(string, index):
	value = ""
	for  x in reversed(range(0, index)):
		if (not string[x].isdigit() and not string[x] == "-" and not string[x] == "."):
				break


		value+= string[x]
		if(string[x] == "-"):
			break
	return (value [::-1])

#Method to find a full number directly after an index and return its String value
def numAfter(string, index):
	value = ""
	for x in (range(index + 1 , len(string))):
		if (not string[x].isdigit() and not string[x] == "."):
			if (value == "" and string[x] == "-"):
				value+= string[x]
			else:
				break
		else:
			value+= string[x]
	return (value)
	
#Method to remove whitespace and simplify calculations
def fixInput(string):
	string = string.replace(" ", "")
	string = string.replace("--", "+")
	string = string.replace("+-", "-")
	return string

#Method that takes in a string and simplifies all subtraction with string operations
def subtraction(string):
	string = fixInput(string)
	index = findCharacter(string, '-')
	if(index == -1 or string.lstrip(".").lstrip('-').isdigit()):
		string = addition(string)
		return string
	if(index == 0):
		index = findCharacter(string[1:], '-') + 1
		if (index == 0):
			string = addition(string)
			return string
	num1 = numBefore(string, index)
	num2 = numAfter(string, index)
	diff = Decimal(num1) - Decimal(num2)
	temp = string[index-len(num1):index + len(num2) + 1]
	string = string.replace(temp, str(diff), 1)
	return subtraction(string)

#Method that takes in a string and simplifies all addition with string operations
def addition(string):
	string = fixInput(string)
	index = findCharacter(string, '+')
	if(index == -1):
		return string
	if(index == 0):
		return string[1:]
	num1 = numBefore(string, index)
	num2 = numAfter(string, index)
	sum = Decimal(num1) + Decimal(num2)
	temp = string[index-len(num1):index + len(num2) + 1]
	string = string.replace(temp, str(sum), 1)
	return addition(string)	

#Method that takes in a string and simplifies all multiplication with string operations
def multiplication(string):
	string = fixInput(string)
	index = findCharacter(string, '*')
	if(index == -1):
		string = subtraction(string)
		return string
	num1 = numBefore(string, index)
	num2 = numAfter(string, index)
	product = Decimal(num1) * Decimal(num2)
	temp = string[index-len(num1):index + len(num2) + 1]
	string = string.replace(temp, str(product), 1)
	return multiplication(string)	

#Method that takes in a string and simplifies all division with string operations
def division(string):
	string = fixInput(string)
	index = findCharacter(string, '/')
	if(index == -1):
		string = multiplication(string)
		return string
	num1 = numBefore(string, index)
	num2 = numAfter(string, index)
	if(num2 == "0"):
		print("Divide by Zero Error")
		quit()
	quotient = Decimal(num1) / Decimal(num2)
	temp = string[index-len(num1):index + len(num2) + 1]
	string = string.replace(temp, str(quotient), 1)
	return division(string)

#Method that takes in a string and simplifies all exponents with string operations	
def power(string):
	string = fixInput(string)
	index = findCharacter(string, '^')
	if(index == -1):
		string = division(string)
		return string
	num1 = numBefore(string, index)
	num2 = numAfter(string, index)
	result = pow(Decimal(num1), Decimal(num2))
	temp = string[index-len(num1):index + len(num2) + 1]
	string = string.replace(temp, str(result), 1)
	return power(string)

#Method that takes in a string and simplifies all parenthesis with string operations. Recursively calls back other methods and will return the final product
def evaluate(string):
	string = fixInput(string)
	inner = findCharacter(string, '(')
	if (inner == -1):
		return power(string)
	count = 1
	outer = 0
	for x in range (inner + 1, len(string)):
		if(string[x] == '('):
			count = count + 1
		elif (string[x] == ')'):
			count = count - 1
		if (count == 0):
			outer = x
			break
	if (count != 0):
		print("Parenthesis Error")
		quit()
	temp = string[inner:outer + 1]
	string = string.replace(temp, evaluate(temp[1:len(temp) - 1]))
	return evaluate(string)

#Loop that scans from terminal
expression = ""
prev = "0"
while(expression != "q"):
	expression = input("Accepted Operators: +, -, *, /, ^ (), Numbers/Decimals, and ANS (Previous Answer)\nEnter in an expression or q to quit: ")
	if ("ANS" in expression):
		expression = expression.replace("ANS", prev)
	ans = evaluate(expression)
	print(ans + "\n")	
	prev = ans
