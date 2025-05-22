import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

# A dictionary to store all the URLs

sport_team_urls = {
						'mens_volleyball': ['https://ccnyathletics.com/sports/mens-volleyball/roster', # City College of New York (Process 1)
											'https://lehmanathletics.com/sports/mens-volleyball/roster', # Lehman College (Process 1)
											'https://www.brooklyncollegeathletics.com/sports/mens-volleyball/roster', # Brooklyn College (Process 1)
											'https://johnjayathletics.com/sports/mens-volleyball/roster', # John Jay College (Process 1)
											'https://athletics.baruch.cuny.edu/sports/mens-volleyball/roster', # Baruch College (Process 1)
											# Medgar Evars College URL not found
											'https://www.huntercollegeathletics.com/sports/mens-volleyball/roster', # Hunter College (Process 1)
											'https://yorkathletics.com/sports/mens-volleyball/roster', # York College (Process 1)
											#'https://ballstatesports.com/sports/mens-volleyball/roster' # Ball State (doesn't match usual HTML)
											],

						'womens_volleyball': [#'https://bmccathletics.com/sports/womens-volleyball/roster', # BMCC (Heights aren't available)
											  #'https://yorkathletics.com/sports/womens-volleyball/roster', # York College (Process 1)
											  #'https://hostosathletics.com/sports/womens-volleyball/roster', # Hostos CC (Heights aren't available)
											  'https://bronxbroncos.com/sports/womens-volleyball/roster/2021', # Bronx CC (Process 2)
											  'https://queensknights.com/sports/womens-volleyball/roster', # Queens College (Process 2)
											  'https://augustajags.com/sports/wvball/roster', # Augusta College (Process 2)
											  'https://flaglerathletics.com/sports/womens-volleyball/roster', # Flagler College (Process 2)
											  #'https://pacersports.com/sports/womens-volleyball/roster', # USC Aiken (Process 1)
											  'https://www.golhu.com/sports/womens-volleyball/roster' # Penn State - Lock Haven (Process 2)
											],

						'mens_swimming_and_diving': ['https://csidolphins.com/sports/mens-swimming-and-diving/roster', # College of Staten Island (Process 2)
													 #'yorkathletics.com/sports/mens-swimming-and-diving/roster', # York College (Process 1)
													 #'https://athletics.baruch.cuny.edu/sports/mens-swimming-and-diving/roster', # Baruch College (Process 1)
													 'https://www.brooklyncollegeathletics.com/sports/mens-swimming-and-diving/roster', # Brooklyn College (Process 2)
													 #'https://lindenwoodlions.com/sports/mens-swimming-and-diving/roster', # Lindenwood University (Process 1)
													 'https://mckbearcats.com/sports/mens-swimming-and-diving/roster', # Mckendree University (Process 2)
													 'https://ramapoathletics.com/sports/mens-swimming-and-diving/roster', # Ramapo College (Process 2)
													 #'https://oneontaathletics.com/sports/mens-swimming-and-diving/roster', # SUNY Oneonta (Process 3?)
													 'https://binghamtonbearcats.com/sports/mens-swimming-and-diving/roster/2021-22', # SUNY Binghampton (Process 2)
													 'https://albrightathletics.com/sports/mens-swimming-and-diving/roster/2021-22' # Albright College (Process 2)
													],

						'womens_swimming_and_diving': ['https://csidolphins.com/sports/womens-swimming-and-diving/roster', # College of Staten Island (Process 2)
													   #'https://queensknights.com/sports/womens-swimming-and-diving/roster', # Queens College (Process 3?)
													   #'https://yorkathletics.com/sports/womens-swimming-and-diving/roster', # York College (Process 1)
													   'https://athletics.baruch.cuny.edu/sports/womens-swimming-and-diving/roster/2021-22?path=wswim', # Baruch College (Process 2)
													   'https://www.brooklyncollegeathletics.com/sports/womens-swimming-and-diving/roster', # Brooklyn College (Process 2)
													   'https://lindenwoodlions.com/sports/womens-swimming-and-diving/roster', # Lindenwood University (Process 2)
													   'https://mckbearcats.com/sports/womens-swimming-and-diving/roster', # Mckendree University (Process 2)
													   'https://ramapoathletics.com/sports/womens-swimming-and-diving/roster', # Ramapo College (Process 2)
													   'https://keanathletics.com/sports/womens-swimming-and-diving/roster', # Kean University (Process 2)
													   #'https://oneontaathletics.com/sports/womens-swimming-and-diving/roster' # SUNY Oneonta (Process 3?)
													]

					}


def process_data_1(urls):

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



def process_data_2(urls):

	names = []
	heights = []

	for url in urls:
		page = requests.get(url)

		if page.status_code == 200:

			soup = BeautifulSoup(page.content,'html.parser')

			height_tags = soup.select("span.sidearm-roster-player-height")
			name_tags = soup.select("div.sidearm-roster-player-name a")


			for name_tag, height_tag in zip(name_tags, height_tags):
				names.append(name_tag.get_text().strip())

				raw_height = height_tag.get_text()

				feet = float(raw_height.split("'")[0]) * 12
				inches = float(raw_height.split("'")[1].replace('"',''))

				height_in_inches = feet + inches
				heights.append(height_in_inches)


	data = {
				'Name' : names,
				'Height' : heights
			}

	df = pd.DataFrame(data)

	avg_height = sum(heights) / len(heights) if heights else 0

	return df, avg_height


mens_volleyball_df, mens_volleyball_avg_height = process_data_1(sport_team_urls['mens_volleyball'])
mens_volleyball_df.to_csv('mens_volleyball.csv')

womens_volleyball_df, womens_volleyball_avg_height = process_data_2(sport_team_urls['womens_volleyball'])
womens_volleyball_df.to_csv('womens_volleyball.csv')

mens_swimming_and_diving_df, mens_swimming_and_diving_avg_height = process_data_2(sport_team_urls['mens_swimming_and_diving'])
mens_swimming_and_diving_df.to_csv('mens_swimming.csv')

womens_swimming_and_diving_df, womens_swimming_and_diving_avg_height = process_data_2(sport_team_urls['mens_swimming_and_diving'])
womens_swimming_and_diving_df.to_csv('womens_swimming.csv')

def get_top_bottom(df):
	shortest = df.nsmallest(5, 'Height')
	tallest = df.nlargest(5, 'Height')
	return shortest, tallest

shortest_men_volleyball, tallest_men_volleyball = get_top_bottom(mens_volleyball_df)
shortest_women_volleyball, tallest_women_volleyball = get_top_bottom(womens_volleyball_df)
shortest_men_swimming, tallest_men_swimming = get_top_bottom(mens_swimming_and_diving_df)
shortest_women_swimming, tallest_women_swimming = get_top_bottom(womens_swimming_and_diving_df)

print("Top 5 Tallest Men's Volleyball Players:\n", tallest_men_volleyball, "\n")
print("Top 5 Shortest Men's Volleyball Players:\n", shortest_men_volleyball, "\n")

print("Top 5 Tallest Women's Volleyball Players:\n", tallest_women_volleyball, "\n")
print("Top 5 Shortest Women's Volleyball Players:\n", shortest_women_volleyball, "\n")

print("Top 5 Tallest Men's Swimming and Diving Athletes:\n", tallest_men_swimming, "\n")
print("Top 5 Shortest Men's Swimming and Diving Athletes:\n", shortest_men_swimming, "\n")

print("Top 5 Tallest Women's Swimming and Diving Athletes:\n", tallest_women_swimming, "\n")
print("Top 5 Shortest Women's Swimming and Diving Athletes:\n", shortest_women_swimming, "\n")