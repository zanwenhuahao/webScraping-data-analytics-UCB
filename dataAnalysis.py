import pandas as pnd

coloradoU_df = pnd.read_csv("UCB_Student_Results-Sheet1.csv")

#print (coloradoU_df.head(10))

#print the dataframe info

print (coloradoU_df.info())

#Get the number of unique majors amongst students
unique_Majors = coloradoU_df['Major'].unique().tolist()
num_of_majors = len(unique_Majors)

#print(unique_Majors)
print("There are " + str(num_of_majors) + " different majors.")

#Count number of students in each major
num_in_each_major = coloradoU_df['Major'].value_counts()
#num_in_each_major.to_csv("majors_info.csv")

#Get all rows that are grad students, based on if the student has a mailbox.
	#print (coloradoU_df[coloradoU_df['Miscellaneous'].str.contains('Mailing Box:') == True])
	#print (coloradoU_df[coloradoU_df['Mailbox'].str.contains('Mailing Box:') == True])
	#print(coloradoU_df[coloradoU_df['Mailbox'].str.contains('Mailing Box:') == True].count())
	#print(len(coloradoU_df[coloradoU_df['Mailbox'].str.contains('Mailing Box:') == True].index))

grad_proper_format = len(coloradoU_df[coloradoU_df['Mailbox'].str.contains('Mailing Box:') == True].index)
grad_improper_format = len(coloradoU_df[coloradoU_df['Miscellaneous'].str.contains('Mailing Box:') == True].index)

total_grad = grad_improper_format + grad_proper_format
total_undergrad = len(coloradoU_df.index) - total_grad

#print the number of grads and undergrads at UCB
print("There are a total of " + str(total_grad) + " grad students.")
print("There are a total of " + str(total_undergrad) + " undergrad students.")

#drop all the rows with bad form that contains "Department:"
coloradoU_df_no_bad_form = coloradoU_df.drop(coloradoU_df[coloradoU_df['Email'].str.contains('Department:') == True].index)
#print(coloradoU_df_no_bad_form.info())

#Find all the rows that have Department info in the wrong place, these are bad form rows.
badform_df = coloradoU_df[coloradoU_df['Email'].str.contains('Department:') == True]
#print(badform_df)
badform_df.to_csv("badformat_info.csv")
#Processing the bad form rows to get good form
goodform_df = badform_df
goodform_df.columns = ['Name', 'Title', 'Major', 'Department', 'Email', 'Mailbox']

goodform_col_list = goodform_df.columns.tolist()
goodform_col_list.remove(goodform_col_list[3])
goodform_col_list.append('Department')

#print(goodform_col_list)
goodform_df = goodform_df[goodform_col_list]

#print(goodform_df)
goodform_df.to_csv("goodformat_info.csv")

#Changing the main dataset's column headings
coloradoU_df_no_bad_form.columns = ['Name', 'Title', 'Major', 'Email', 'Mailbox', 'Department']
coloradoU_result = pnd.concat([coloradoU_df_no_bad_form, goodform_df])

#print(coloradoU_result.info())
coloradoU_result.to_csv("UCB_Student_Results-Cleaned.csv")

#Processing the majors document to get some info
Majors_df = pnd.read_csv("majors_info.csv")

Engineering_df = Majors_df[Majors_df['Major'].str.contains('Engineering|Computer Science') == True]
Total_Engineering_Majors = str(Engineering_df['Number of Student'].sum(axis = 0))
print(Engineering_df)


Biz_df = Majors_df[Majors_df['Major'].str.contains('Economics|Finance|Business|Manage|MBA|Accounting|Marketing') == True]
total_biz_majors = str(Biz_df['Number of Student'].sum(axis = 0))
print(Biz_df)


Education_df = Majors_df[Majors_df['Major'].str.contains('Educ') == True]
total_educ_majors = str(Education_df['Number of Student'].sum(axis = 0))
print(Education_df)


Sciences_df = Majors_df[Majors_df['Major'].str.contains('Biology|Chemistry|Physiology|Psychology|Physics|Astronomy|Environmental Studies|Geology') == True]
Total_Sci_Majors = str(Sciences_df['Number of Student'].sum(axis = 0))
print(Sciences_df)


Fine_Arts_df = Majors_df[Majors_df['Major'].str.contains('Art History|Arts|Music|Dance|Theatre|Media') == True]
Total_Fine_Arts_Majors = str(Fine_Arts_df['Number of Student'].sum())
print(Fine_Arts_df)


Liberal_Arts_df = Majors_df[Majors_df['Major'].str.contains('Sociology|Geography|History|Anthropology|Studies|Humanities|Classic|Literature') == True]
Total_Liberal_Arts_Majors = str(Liberal_Arts_df['Number of Student'].sum())
print(Liberal_Arts_df)

print("There are a total of " + Total_Engineering_Majors + " Engineering Majors")
print("There are a total of " + total_biz_majors + " Business Majors")
print("There are a total of " + total_educ_majors + " Education Majors")
print("There are a total of " + Total_Sci_Majors + " Science Majors")
print("There are a total of " + Total_Fine_Arts_Majors + " Fine Arts Majors")
print("There are a total of " + Total_Liberal_Arts_Majors + " Liberal Arts Majors")

#Cleaning the name field in the table into first middle last names fields
coloradoU_result['firstName'] = coloradoU_result['Name'].str.split().str[0].str.strip()
coloradoU_result['lastName'] = coloradoU_result['Name'].str.split().str[-1].str.strip()
coloradoU_result['middleName'] = coloradoU_result['Name'].str.split(' ', 1).str[1].str.strip()
coloradoU_result['middleName'] = coloradoU_result['middleName'].str.rsplit(' ', 1).str[0].str.strip()
coloradoU_result['middleName'] = coloradoU_result['middleName'].mask(coloradoU_result['middleName'] == coloradoU_result['lastName'], "")
print(coloradoU_result.head(10))


new_columns = ['firstName', 'middleName', 'lastName', 'Title', 'Major', 'Email', 'Mailbox', 'Department']
coloradoU_name_cleaned = coloradoU_result[new_columns]
print(coloradoU_name_cleaned.head(10))
coloradoU_name_cleaned.to_csv("UCB_student_results_final.csv")

