import csv
import time
from random import randint
import requests
from bs4 import BeautifulSoup
import Helper as hlp

# Url
url = "https://www.imdb.com/search/title?release_date=2017-01-01,2018-12-26&sort=num_votes,desc&start=1&ref_=adv_nxt"

# Get the response
response = requests.get(url)

# Make Soup
soup = BeautifulSoup(response.text, "html.parser")

# Get the data

# Initial Scrape data
names = []
durations = []
years = []
ratings = []
metascores = []
votes = []
total_gross = []

# Create the initial file
with open("data/movie.csv", "w", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Year", "Duration", "Rating", "MetaScore", "Vote", "Gross"])

# Fetch the data
lister_items = soup.find_all("div", class_="lister-item")

for single_item in lister_items:
    single_item_content = single_item.find("div", class_="lister-item-content")

    # Extract the data
    # Movie Name
    name = single_item_content.h3.a.get_text()
    # Movie Time
    duration = single_item_content.find("p", class_="text-muted").find("span", class_="runtime").get_text()
    # When the movie has been released
    year = single_item_content.h3.find("span", class_="lister-item-year").get_text()
    # Movie total rating
    rating = single_item_content.find("div", class_="ratings-imdb-rating")["data-value"]
    # Metascore
    metascore = single_item_content.find("div", class_="ratings-metascore")
    if metascore is not None:
        metascore = metascore.span.get_text()
    else:
        metascore = "Unknown"
    # Vote & Income
    vote_gross = single_item_content.find("p", class_="sort-num_votes-visible").find_all("span", attrs={"name": "nv"})
    vote = vote_gross[0]["data-value"]
    if len(vote_gross) > 1:
        gross = vote_gross[1]["data-value"]
    else:
        gross = "Unknown"

    # Clean the data
    name = hlp.clean(name)
    duration = hlp.clean_duration(duration)
    year = hlp.clean_year(year)
    rating = float(hlp.clean(rating))
    metascore = hlp.metascore_to_int(hlp.clean(metascore))
    vote = int(hlp.clean(vote))
    gross = hlp.clean_gross(gross)

    # Save the data
    with open("data/movie.csv", "a", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([name, year, duration, rating, metascore, vote, gross])
        print("{} is added to csv".format(name))
