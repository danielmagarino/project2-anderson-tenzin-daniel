import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt


# A dictionary to store all the URLs

sport_team_urls = {
						'mens_volleyball': ['https://ccnyathletics.com/sports/mens-volleyball/roster', # City College of New York
											'https://lehmanathletics.com/sports/mens-volleyball/roster', # Lehman College
											'https://www.brooklyncollegeathletics.com/sports/mens-volleyball/roster', # Brooklyn College
											'https://johnjayathletics.com/sports/mens-volleyball/roster', # John Jay College
											'https://athletics.baruch.cuny.edu/sports/mens-volleyball/roster', # Baruch College
											# Medgar Evars College URL not found
											'https://www.huntercollegeathletics.com/sports/mens-volleyball/roster', # Hunter College
											'https://yorkathletics.com/sports/mens-volleyball/roster', # York College
											#'https://ballstatesports.com/sports/mens-volleyball/roster' # Ball State (doesn't match usual HTML)
											],

						'womens_volleyball': [#'https://bmccathletics.com/sports/womens-volleyball/roster', # BMCC (Heights aren't available)
											  'https://yorkathletics.com/sports/womens-volleyball/roster', # York College
											  #'https://hostosathletics.com/sports/womens-volleyball/roster', # Hostos CC (Heights aren't available)
											  #'https://bronxbroncos.com/sports/womens-volleyball/roster/2021', # Bronx CC (doesn't match default process)
											  #'https://queensknights.com/sports/womens-volleyball/roster', # Queens College (doesn't match default process)
											  'https://augustajags.com/sports/wvball/roster', # Augusta College
											  'https://flaglerathletics.com/sports/womens-volleyball/roster', # Flagler College
											  'https://pacersports.com/sports/womens-volleyball/roster', # USC Aiken
											  'https://www.golhu.com/sports/womens-volleyball/roster' # Penn State - Lock Haven
											],

						'mens_swimming_and_diving': ['https://csidolphins.com/sports/mens-swimming-and-diving/roster', # College of Staten Island
													 'yorkathletics.com/sports/mens-swimming-and-diving/roster', # York College
													 'https://athletics.baruch.cuny.edu/sports/mens-swimming-and-diving/roster', # Baruch College
													 'https://www.brooklyncollegeathletics.com/sports/mens-swimming-and-diving/roster', # Brooklyn College
													 'https://lindenwoodlions.com/sports/mens-swimming-and-diving/roster', # Lindenwood University
													 'https://mckbearcats.com/sports/mens-swimming-and-diving/roster', # Mckendree University
													 'https://ramapoathletics.com/sports/mens-swimming-and-diving/roster', # Ramapo College
													 'https://oneontaathletics.com/sports/mens-swimming-and-diving/roster', # SUNY Oneonta
													 'https://binghamtonbearcats.com/sports/mens-swimming-and-diving/roster/2021-22', # SUNY Binghampton
													 'https://albrightathletics.com/sports/mens-swimming-and-diving/roster/2021-22' # Albright College
													],

						'womens_swimming_and_diving': ['https://csidolphins.com/sports/womens-swimming-and-diving/roster', # College of Staten Island
													   'https://queensknights.com/sports/womens-swimming-and-diving/roster', # Queens College
													   'https://yorkathletics.com/sports/womens-swimming-and-diving/roster', # York College
													   'https://athletics.baruch.cuny.edu/sports/womens-swimming-and-diving/roster/2021-22?path=wswim', # Baruch College
													   'https://www.brooklyncollegeathletics.com/sports/womens-swimming-and-diving/roster', # Brooklyn College
													   'https://lindenwoodlions.com/sports/womens-swimming-and-diving/roster', # Lindenwood University
													   'https://mckbearcats.com/sports/womens-swimming-and-diving/roster', # Mckendree University
													   'https://ramapoathletics.com/sports/womens-swimming-and-diving/roster', # Ramapo College
													   'https://keanathletics.com/sports/womens-swimming-and-diving/roster', # Kean University
													   'https://oneontaathletics.com/sports/womens-swimming-and-diving/roster' # SUNY Oneonta
													]

					}




'''
### A DIFFERENT SCRAPING PROCESS ###
# Works for: Bronx CC (womens volleyball)

page = requests.get("https://bronxbroncos.com/sports/womens-volleyball/roster/2021")

if page.status_code == 200:

  soup = BeautifulSoup(page.content,'html.parser')

  names = soup.select("div.sidearm-roster-player-name a")
  heights = soup.select("span.sidearm-roster-player-height")

  # Removes the strange repetition of heights
  heights = heights[:len(names)]

for name in names:
    print(name.text.strip())

for height in heights:
    print(height.text.strip())

'''



'''
### ANOTHER SCRAPING PROCESS ###
# (Almost) Works for: Queens College (womens volleyball)
# The first and last names are separate I'm trying to put them together

firstnames = []
lastnames = []
names = []
heights = []

page = requests.get("https://queensknights.com/sports/womens-volleyball/roster")

if page.status_code == 200:

  soup = BeautifulSoup(page.content,'html.parser')

  first_name_span = soup.select("span.sidearm-roster-player-first-name")
  last_name_span = soup.select("span.sidearm-roster-player-last-name")

  heights = soup.select("span.sidearm-roster-player-height")

  for x in first_name_span:
      firstnames.append(x.text.strip())

  for x in last_name_span:
      lastnames.append(x.text.strip())

  names = [f"{first} {last}" for first, last in zip(firstnames, lastnames)]
  print(names)

  for height in heights:
      print(height.text.strip())
'''

def process_data(urls):

	names = []
	heights = []

	for url in urls:
		page = requests.get(url)

		if page.status_code == 200:

			soup = BeautifulSoup(page.content,'html.parser')

			height_tags = soup.find_all('td', class_='height')
			name_tags = soup.find_all('td', class_='sidearm-table-player-name')

			for name_tag in name_tags:
				names.append(name_tag.get_text().strip())

			for height_tag in height_tags:
				raw_height = height_tag.get_text()

				feet = float(raw_height.split('-')[0]) * 12
				inches = float(raw_height.split('-')[1])

				height_in_inches = feet + inches
				heights.append(height_in_inches)

	data = {
				'Name' : names,
				'Height' : heights
			}

	df = pd.DataFrame(data)
	avg_height = sum(heights) / len(heights)

	return df, avg_height

mens_volleyball_df, mens_volleyball_avg_height = process_data(sport_team_urls['mens_volleyball'])

mens_volleyball_df