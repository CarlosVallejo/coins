


string1 = ["50 peniques","quarter", "1 medio pene"]

for string in string1:

	if string[:2] == "1 ":
		string = string.replace("1 ", "")

	string_list = string.split(' ', 1)

	if len(string_list) == 2:
		print "In: ", string

	else:

		print "out: ", string_list[0]

