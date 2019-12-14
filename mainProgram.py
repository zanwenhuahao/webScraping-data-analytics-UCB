import scraper
from string import ascii_lowercase


keyword = ""

write_file = "resultsH_Z.csv"
file_heading = [["Name","Title","Major","Email","Mailbox"]]
temp_file = "temp_with_duplicates.csv"

scraper.csv_write(write_file, file_heading)

#For storing the results from the following for-loops at completion
result_set = set()
result_a_lst = []

for first_letter in ascii_lowercase:
	if first_letter < 'h':
		continue
	for second_letter in ascii_lowercase:
		for third_letter in ascii_lowercase:
			keyword = first_letter + second_letter + third_letter

			#INFO: print out current keyword being searched
			print("INFO: currently searching: " + keyword)

			result_a_lst = scraper.keyword_search(keyword)

			#INFO: Print out each result_a_lst for each keyword searched.
			#scraper.pretty_list_printer(result_a_lst)

			for each in result_a_lst:
				result_set.add(tuple(each))
			scraper.csv_write(temp_file, result_a_lst)

scraper.csv_write(write_file, list(result_set))
print("program finished without error")