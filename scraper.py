import requests
import csv
from bs4 import BeautifulSoup

#helper functions
#get rid of newlines in the list of html info produced by .children function from soup
def clean_newlines(lst):
	cleanlst = []
	for each in lst:
		if each != '\n':
			cleanlst.append(each)
	return cleanlst

#clean out specific words from data we don't want
def clean_data(keyword, lst):
	for each in lst:
		if(keyword == each):
			lst.delete(each)

#Get only 'student' results from total list of people found
def get_only_student(lst):
	all_student = []
	for each in lst:
		if each[1] == 'Student':
			all_student.append(each)
		#INFO see each student entry
		#else:
			#print(each)
	return all_student

#Clean each student data form
def clean_student_info(lst):
	for each in lst:
		if 'Major:' in each[2]:
			each[2] = each[2].replace('Major: ', "")
		else:
			each.insert(2,"")

#Add column heading to a list
def add_headings(headingLst, lst):
	lst.insert(0,headingLst)

#List Pretty Printer - prints each thing in lst on a separate line
def pretty_list_printer(lst):
	for each in lst:
		print(each)

#Write list info to CSV
def csv_write(filename,lst):
	with open(filename, 'a', newline='') as file:
		CSVwriter = csv.writer(file)
		CSVwriter.writerows(lst)
	file.close()



#Trying a random keyword lastname
def keyword_search(keyword):
	#setting up request URL
	baseURL_head = "https://www.colorado.edu/search?cse="
	baseURL_tail = "&op=Search"

	cseKeyword = keyword

	requestURL = baseURL_head+cseKeyword+baseURL_tail

	#get the request page
	page = requests.get(requestURL)
	#Success, page returns code 200
	#print(page.content)

	#---------- Soup ---------------

	soup = BeautifulSoup(page.content, 'html.parser')
	#print(soup.prettify())

	all_people = []
	#returns a list of people found, given by the following class.
	if (soup.find_all('li', attrs={"class":"cu-directory-sidebar-result people-result"})):
		peopleList = soup.find_all('li', attrs={"class":"cu-directory-sidebar-result people-result"})
		#print(peopleList)

		#INFO: return the number of people found in search
		#print("There are " + str(len(peopleList)) + " people found in search.")

		for x in range(len(peopleList)):
			person_data = []

			name = peopleList[x].find('a', {"class":"people-more"}).get_text().strip()
			person_data.append(name)

			title = peopleList[x].find('div', {"class":"people-title"}).get_text().strip()
			person_data.append(title)

			otherInfo = peopleList[x].find('div', {"class":"people-meta"})
			#rint(otherInfo)
			otherInfo_list = list(otherInfo.children)
			#print(otherInfo_list)
			#print(otherInfo_list[1])
			#print(otherInfo_list[1].get_text())

			for each in otherInfo_list:
				if(each != '\n'):
					if(each.find('a',{"class":"email-long"})):
						person_data.append(each.find('a',{"class":"email-long"}).get_text())
					else:
						person_data.append(each.get_text())
			#print(person_data)
			all_people.append(person_data)

		#INFO: return the number of people found in search whose results have been parsed
		#print("Number of people retrieved: " + str(len(all_people)))
		all_people = get_only_student(all_people)
		#INFO: return the number of STUDENTS found in search
		#print("Number of STUDENTS retrieved: " + str(len(all_people)))

		clean_student_info(all_people)

		#INFO: prints each student's data as a list on a separate line
		#pretty_list_printer(all_people)

		#csv_write(filename, all_people)
		
	return all_people