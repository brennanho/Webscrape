#Univseral helper file for various webcrawling/webscraping tasks

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import  bs4, time, csv, re, urllib.request, random, sys, os, urllib, subprocess


def convert_none(tag):
	if tag is None:
		return ""
	else: 
		return tag.get_text()

def init_chrome_driver(headless=False):
	if headless:
		chrome_options.add_argument("--headless")
	chrome_options = Options()  
	chrome_options.add_argument("--start-maximized")
	prefs = {"profile.managed_default_content_settings.images": 2, 'disk-cache-size': 4096}
	chrome_options.add_experimental_option('prefs', prefs)
	driver = webdriver.Chrome(chrome_options=chrome_options)
	driver.set_page_load_timeout(60)
	return driver

#selenium
def get_html_page(driver, site, url):
	if site == 'pinnacle' or site == 'wiki':
		try:
			driver.get(url)
		except TimeoutException as e:
			print(e)
	else:
		driver.get(url)
		loaded = len(driver.page_source)
		time.sleep(5)
		while len(driver.page_source) > loaded:
			loaded = len(driver.page_source)
			time.sleep(3)
	
	html = bs4.BeautifulSoup(driver.page_source, 'html.parser') # or 'lxml'
	return html

#urllib 
def get_html_page_static(url):
	f = urllib.request.urlopen(url)
	html = bs4.BeautifulSoup(f.read(), 'html.parser') # or 'lxml'
	return html

def write_to_csv(all_bets, filename):
	with open(filename, "w", newline='') as results_file:
		writer = csv.writer(results_file, delimiter=',')
		writer.writerow(["Time", "Team", "Money Line", "Spread", "Price"])
		for i, bet in enumerate(all_bets):
			writer.writerow(bet)
			# if i % 2 == 0:
			# 	writer.writerow([])