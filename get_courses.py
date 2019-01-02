#Find courses that are not full (no waitlist)

from helpers import init_chrome_driver
import time, sys

#Populate courses to check on myschedule
courses = []
with open("courses.txt","r") as course_file:
	for course in course_file:
		courses.append(course.strip())

browser = init_chrome_driver()
webpage = browser.get('http://myschedule.sfu.ca')
browser.find_element_by_xpath('//*[@id="addCourseButton"]').click()
browser.find_element_by_xpath('//*[@id="term_3201910"]').click()
for course in courses:
	browser.find_element_by_id('code_number').send_keys(course) #Input course name
	browser.find_element_by_xpath('//*[@id="addCourseButton"]').click() #Select course
	
	#Get course info, if full or not
	try:
		seats = browser.find_element_by_xpath('//*[@id="legend_box"]/div[3]/div/div/div/label/div/div[1]/table/tbody/tr[1]/td[2]/span[1]/span').get_attribute('innerHTML').strip()
		print(course, seats)
	except:
		pass

	#Clear last search
	try:
		browser.find_element_by_xpath('//*[@id="requirements"]/div[3]/div[2]/div[1]/a').click()
	except:
		pass

	time.sleep(1)
