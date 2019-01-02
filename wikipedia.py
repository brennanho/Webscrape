#Crawl wikipedia starting from the homepage and log urls visited

from helpers import *

class Wikipedia:
	def __init__(self):
		self.root_page = 'https://en.wikipedia.org'
		self.main_page = 'https://en.wikipedia.org/wiki/Main_Page'
		self.bad_links = ['#mw-head', '#p-search']
		self.driver = init_chrome_driver()
		#self.current_html = get_html_page_static(self.main_page)
		self.current_html = get_html_page(self.driver, 'wiki', self.root_page)
		self.urls = []
		self.all_urls = []
		self.visited_urls = []
		self.page_count = 0

	def get_sublinks(self, html):
		current_urls = []
		for link in html.find_all('a'):
			try:
				url = link['href']
				if url.startswith('/wiki/'):
					url = self.root_page + url
				elif url.startswith('//'):
					url = self.root_page + '/wiki' + url
				elif 'wikipedia.org' not in url:
					continue

				if url not in self.urls and url not in self.bad_links and not url.endswith('.jpeg') and not url.endswith('.jpg') and not url.startswith('/w/') and not url.startswith('#'):
					current_urls.append(url)
					self.urls.append(url)
					self.page_count += 1

			except:
				pass
		self.all_urls.append(current_urls)
		return current_urls

	def get_next_html_page(self, html):
		current_urls = self.get_sublinks(html)
		while True:
			
			#No links on current page -> go to previous page
			while len(current_urls) == 0:
				current_urls = self.all_urls.pop(-1)
			
			current_url = random.choice(current_urls)
			try:
				#next_html = get_html_page_static(current_url)
				next_html = get_html_page(self.driver, 'wiki', current_url)
			except:
				current_urls.remove(current_url)
				continue

			self.visited_urls.append(current_url)
			return current_url, next_html

	def start_crawling(self):
		html = self.current_html
		while True:
			current_path, html = self.get_next_html_page(html)
			log = "Total pages: " + str(self.page_count) + " Path count: " + str(len(self.visited_urls)) + " " + current_path
			print(log)
			os.system('echo ' + log + ' >> wiki_logs')

if __name__ == "__main__":
	wiki = Wikipedia()
	wiki.start_crawling()
