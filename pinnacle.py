#Scrape and record CSV data of bet odds on pinnacle.com

from helpers import *

class Pinnacle:
	def __init__(self):
		self.sports_titles = []
		self.sublinks = []
		self.all_bets = []
		self.driver = init_chrome_driver()
		self.root_url = 'https://www.pinnacle.com'
		self.html = get_html_page(self.driver, 'pinnacle', self.root_url)

	def get_sports_titles(self):
		for tag in self.html.find_all('li',{'class':'level-2 collapse'}):
			for span in tag.find('span'):
				try:
					self.sports_titles.append(span['title'])
				except:
					pass

		#format titles appropriate for url		
		self.sports_titles = ['e-sports' if title=='eSports' else title.lower() for title in self.sports_titles]
		for i, title in enumerate(self.sports_titles):
			title = ['-' if c==' ' else c for c in title]
			title = ''.join(str(c) for c in title)
			self.sports_titles[i] = title

		self.sports_titles = list(set(self.sports_titles))
		return self.sports_titles

	def get_sublinks(self, category):
		for link in self.html.find_all('a'):
			try:
				#configured for esports at the moment
				sublink = "/en/odds/match/" + category + "/"
				if sublink in link['href']:
					if self.root_url not in link['href']:
						link = self.root_url + link['href']
						self.sublinks.append(link)
					else:
						self.sublinks.append(link['href'])
			except:
				pass

		self.sublinks = list(set(self.sublinks))
		return self.sublinks

	def get_bet_stats(self, url):
		html = get_html_page(self.driver, 'pinnacle', url)
		bets = []
		teams = [team for team in html.find_all('tr',{'ng-repeat':'participant in participants = (event.Participants)'},{'class':'ng-scope'})]

		for i, team in enumerate(teams):
			name = convert_none(team.find('span', {'ng-if':'participant.Name != undefined'}, {'class':'ng-binding ng-scope'}))
			money_line = convert_none(team.find('span', {'ng-if':'participant.MoneyLine != undefined && !isOffline(event)'}, {'class':'ng-binding ng-scope'}))
			spread = convert_none(team.find('span', {'class':'spread ng-binding'}))
			price = convert_none(team.find('span', {'class':'price ng-binding'}))

			if i % 2 == 0: 
				time = convert_none(team.find('span', {'class':'ng-binding'})).replace(".",":")

			bets.append([time, name, money_line, spread, price])

		return bets

	def get_all_bet_stats(self, category):
		self.today_url = self.root_url + '/en/odds/today/' + category + '/'
		self.html = get_html_page(self.driver, 'pinnacle', self.today_url)
		self.sublinks = self.get_sublinks(category)

		for link_count, link in enumerate(self.sublinks, 1):
			bet_stats = self.get_bet_stats(link)
			if len(bet_stats) == 0:
				print("\nLink",str(link_count) + "/" + str(len(self.sublinks)) + ":","failed to retrieve data from", link, "\n")
				continue

			self.all_bets.append(bet_stats)
			print("\nLink",str(link_count) + "/" + str(len(self.sublinks)) + ":","retrieved data from", link, "\n")

		flatten_all_stats = [bets for sublist in self.all_bets for bets in sublist]
		return flatten_all_stats

if __name__ == "__main__":
	pinnacle = Pinnacle()

	#all_bets = pinnacle.get_bet_stats('https://www.pinnacle.com/en/odds/today/e-sports')
	all_bets = pinnacle.get_all_bet_stats('e-sports')

	# all_bets = pinnacle.get_all_bet_stats('e-sports')
	all_bets = pinnacle.get_all_bet_stats('basketball')
	write_to_csv(all_bets, 'pinnacle.csv')
	
	# big_cvs = []
	# for sport in pinnacle.get_sports_titles():
	# 	print("\nPulling",sport, "data...\n")
	# 	all_bets = pinnacle.get_all_bet_stats(sport)
	# 	big_cvs.append(all_bets)
	# flatten_big_csv = [bets for sublist in big_cvs for bets in sublist]
	# write_to_csv(flatten_big_csv, 'pinnacle.csv')

	pinnacle.driver.quit()