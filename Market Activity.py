import requests
from bs4 import BeautifulSoup
import pandas as pd

Companies=[]
Tickers=[]
GICS_Sectors=[]
GICS_Sub_Industries=[]
url='https://en.m.wikipedia.org/wiki/Nasdaq-100#External_links'
website=requests.get(url)
if website.status_code==200:
	soup=BeautifulSoup(website.content,'html.parser')
	t_tag=soup.find('table',id='constituents')
	rows=t_tag.find_all('tr')
	for row in rows:
		cells= row.find_all('td')
		if len(cells)==4:
			Companies.append(cells[0].get_text())
			Tickers.append(cells[1].get_text())
			GICS_Sectors.append(cells[2].get_text())
			GICS_Sub_Industries.append(cells[3].get_text().strip())
	Component_data={
					'Company':Companies,
					'Ticker':Tickers,
					'GICS Sector':GICS_Sectors,
					'GICS Sub-Industry':GICS_Sub_Industries,
				}
	DF1=pd.DataFrame(Component_data)
else:
	print("Invalid status code")

DF1.to_csv("nasdaq_df1.csv", index=False)
print(" Saved nasdaq_df1.csv")
