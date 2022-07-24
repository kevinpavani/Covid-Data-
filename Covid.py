import pandas as pd
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import texttable as tt
import requests
from bs4 import BeautifulSoup

# URL for scraping data
url = 'https://www.worldometers.info/coronavirus/countries-where-coronavirus-has-spread/'

# get URL html
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

data = []

# soup.find_all('td') will scrape every each element in the url's table
data_iterator = iter(soup.find_all('td'))

# data_iterator is the iterator of the table
# This loop will keep repeating till there is
# data available in the iterator
while True:
	try:
		country = next(data_iterator).text
		cases = next(data_iterator).text
		deaths = next(data_iterator).text
		continent = next(data_iterator).text

		# For 'confirmed' and 'deaths',
		# make sure to remove the commas
		# and convert to int
		data.append((
			country,
			int(cases.replace(',', '')),
			int(deaths.replace(',', '')),
			continent
		))

	# StopIteration error is raised when
	# there are no more elements left to
	# iterate through
	except StopIteration:
		break

# Sort the data by the number of confirmed cases
data.sort(key = lambda row: row[1], reverse = True)

# Save it as Dataframe
covid = pd.DataFrame(data)

# Rename columns
covid.columns =['Country', 'Cases', 'Deaths', 'Continent']

#Inspect Data
print(covid.to_string())


#Rename Japan entry, as it is named Japan (+Diamond Princess)
covid = covid.replace("Japan (+Diamond Princess)", "Japan")

#Save as Excel csv file for later use on Power BI
covid.to_csv('covid_data.csv', index = None)


#Plotting Covid cases
plt.bar(covid['Country'].head(20), covid['Cases'].head(20), color='y', width=0.4)
plt.xlabel("Country")
plt.ylabel("Covid Cases")
plt.xticks(rotation = 90) # Rotates X-Axis Ticks by 90-degrees
plt.show()


#Plotting Covid deaths
plt.bar(covid['Country'].head(20), covid['Deaths'].head(20), color='c', width=0.4)
plt.xlabel("Country")
plt.ylabel("Covid Losses")
plt.xticks(rotation = 90) # Rotates X-Axis Ticks by 90-degrees
plt.show()

