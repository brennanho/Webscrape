from helpers import init_chrome_driver
import time, sys

#Script Purpose: Apply to coop jobs that do not require a cover letter

browser = init_chrome_driver()
webpage = browser.get('https://cas.sfu.ca/cas/login?message=Welcome+to+SFU+myExperience.%20Please+login+with+your+SFU+computing+ID.&allow=student,alumni&renew=true&service=https://myexperience.sfu.ca/sfuLogin.htm%3Faction%3Dlogin')
time.sleep(1)

#Command line arguments
username = sys.argv[1]
password = sys.argv[2]
job_title = sys.argv[3]

#Login to MyExperience
browser.find_element_by_id("username").send_keys(username)
browser.find_element_by_id("password").send_keys(password)
browser.find_element_by_name("submit").click()

#Advanced search settings
browser.get('https://myexperience.sfu.ca/myAccount/co-op/postings.htm')
browser.find_element_by_class_name('orbis-posting-actions').find_element_by_link_text('Advance Search').click()
browser.find_element_by_id('question_Position').send_keys(job_title)

#Go to listings page
browser.find_element_by_link_text('Search Job Postings').submit()

#Itterate through all jobs in the search results
job_table = browser.find_element_by_id('postingsTable').find_element_by_tag_name('tbody')
job_page = browser.window_handles[0]
num_applications = 0
for job in job_table.find_elements_by_tag_name('tr'):
	apply_button = job.find_elements_by_tag_name('a')[1]
	applied_status = job.find_elements_by_tag_name('td')[1].get_attribute('innerHTML').strip()
	apply_button.click()
	browser.switch_to.window(browser.window_handles[len(browser.window_handles)-1])

	try:
		requirements = browser.find_element_by_xpath('//*[@id="postingDiv"]/div[2]/div[2]/table/tbody/tr[2]/td[2]').get_attribute('innerHTML').strip()
	except Exception as e:
		print(e)

	#Apply to job
	if 'Cover Letter' not in requirements and not applied_status:
		try:
			posting_title = browser.find_element_by_xpath('//*[@id="mainContentDiv"]/div[1]/div[1]/div[1]/h1').get_attribute('innerHTML').strip()
			company = browser.find_element_by_xpath('//*[@id="postingDiv"]/div[3]/div[2]/table/tbody/tr[1]/td[2]').get_attribute('innerHTML').strip()
			browser.find_element_by_xpath('//*[@id="mainContentDiv"]/div[2]/div/a[1]').click()
			browser.switch_to.window(browser.window_handles[len(browser.window_handles)-1])
			browser.find_element_by_xpath('//*[@id="applyToPostingForm"]/div/div[2]/div[1]/div[1]/label/input').click()
			time.sleep(2)
			package_radio_buttons = browser.find_element_by_xpath('//*[@id="applyToPostingForm"]/div/div[2]/div[1]/div[2]/table/tbody').find_elements_by_tag_name('tr')
			package_radio_buttons[len(package_radio_buttons)-1].find_elements_by_tag_name('td')[0].find_element_by_tag_name('input').click()
			browser.find_element_by_xpath('//*[@id="applyToPostingForm"]/div/div[2]/input').submit()
			print("APPLIED TO: ", company, posting_title)
			num_applications += 1
		except Exception as e:
			print(e)

	browser.close()
	browser.switch_to.window(job_page)

print("Total applications: ", num_applications)