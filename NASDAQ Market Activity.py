import requests
from bs4 import BeautifulSoup
import pandas as pd

Symbols=[]
Names=[]
Market_Caps=[]
Last_Sales=[]
Net_Change=[]
Percentage_Change=[]
url='https://www.nasdaq.com/market-activity/quotes/nasdaq-ndx-index'
website=requests.get(url)
if content.status_code==200:
	soup=BeautifulSoup(website.content,'html.parser')
	t_tag=soup.find('table')
	rows=t_tag.findall('tr')
	for row in rows:
		cells= row.findall('td')
		if len(cells)==6:
			Symbols.append(cells[0].get_text())
			Names.append(cells[1].get_text())
			Market_Caps.append(cells[2].get_text())
			Last_Sales.append(cells[3].get_text())
			Net_Change.append(cells[4].get_text())
			Percentage_Change.append(cells[5].get_text())
	NASDAQ_data={
					'Symbol':Symbols,
					'Name':Names,
					'Market Cap':Market_Caps,
					'Last Sale':Last_Sales,
					'Net Change':Net_Change,
					'Percentage_Change':Percentage_Change
				}
	DF1=pd.DataFrame(NASDAQ_data)
else:
	print("Invalid status code")