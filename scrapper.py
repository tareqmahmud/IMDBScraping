import time
from random import randint
from warnings import warn

import pandas as pd
import requests
from IPython.core.display import clear_output
from bs4 import BeautifulSoup

from Scraper import Helper as hlp

# Initial Scrape data
names = []
durations = []
years = []
ratings = []
metascores = []
votes = []
total_gross = []

# Monitor time
start_time = time.time()
request = 1
movie_no = 1

for i in range(0, 21):
    # Generate the page
    page = i * 50 + 1

    # Url
    url = "https://www.imdb.com/search/title?release_date=2017-01-01,2018-12-26&sort=num_votes," \
          "desc&start={}&ref_=adv_nxt".format(page)

    # Send the request and Get the response
    response = requests.get(url)

    # Make Soup
    soup = BeautifulSoup(response.text, "html.parser")

    # Fetch the data
    lister_items = soup.find_all("div", class_="lister-item")

    # Get the data
    for single_item in lister_items:
        single_item_content = single_item.find("div", class_="lister-item-content")

        # Extract the data
        # Movie Name
        name = single_item_content.h3.a.get_text()
        # Movie Time
        duration = single_item_content.find("p", class_="text-muted").find("span", class_="runtime")
        if duration is not None:
            duration = duration.get_text()
        else:
            duration = "Unknown"
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
        vote_gross = single_item_content.find("p", class_="sort-num_votes-visible").find_all("span",
                                                                                             attrs={"name": "nv"})
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

        # Add data to global array
        names.append(name)
        durations.append(duration)
        years.append(year)
        ratings.append(rating)
        metascores.append(metascore)
        votes.append(vote)
        total_gross.append(gross)

        print("Movie No. #{}: {} item added to global array".format(movie_no, name))

        # Separate Every Movie
        print("---------------------------------------------------")

        # Increment Movie
        movie_no += 1

    # Monitor Time
    total_time = time.time() - start_time
    request_per_sec = total_time / request
    print("{} request done per sec".format(request_per_sec))

    # If status is not 200 then show an warning with request number
    if response.status_code != 200:
        warn("{} no. has status code {}\n{}\n".format(request, response.status_code, url))

    # Increment Request
    request += 1

    # Sleep for sometime
    print("\n---------------------------------------------------")
    print("\tSleeping")
    rand_sec = randint(1, 30)
    time.sleep(rand_sec)
    print("\tSleep For {}sec".format(rand_sec))
    print("\tGo to the page: {}".format(page))
    print("---------------------------------------------------\n")
    clear_output(wait=True)

# Store the data to csv format
data_frame = pd.DataFrame({
    "Name": names,
    "Year": years,
    "Duration": durations,
    "Rating": ratings,
    "MetaScore": metascores,
    "Vote": votes,
    "Gross": total_gross
})

data_frame.to_csv("data/movie.csv", index=False)
print("All data successfully added")
