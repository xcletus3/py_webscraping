from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import csv

# open csv file
file = open("IlabsWebScrap.csv", 'w')
# writer = csv.writer(file)

# heading
# writer.writerow(['Order No', 'Movie Name', 'Movie Year', 'Movie Content URL', 'Movie Image URL', 'Movie Discription',
#                  'Directors', 'Stars'])
records = []

start = 1
finish = 1000

# Loop for pages
while start < finish:
    URL = f"https://www.imdb.com/search/title/?year=2022&title_type=feature&start={start}&ref_=adv_nxt"
    result = requests.get(URL).text

    # Extract content
    doc = BeautifulSoup(result, "html.parser")
    article = doc.find(class_="article")
    table = article.find(class_="lister-list")
    text = article.find(class_="desc").text

    # Start and End movie numbers
    start = int(re.search(r'\n([,\d]+)-([,\d]+).*', text).group(1).replace(',', ''))
    end = int(re.search(r'\n([,\d]+)-([,\d]+).*', text).group(2).replace(',', ''))

    # Loop for movies
    for i in range(start, end+1):

        # For index Extract through the table
        count = i-start

        # Extract movie details
        movieCard = table.findAll(class_="lister-item")[count]
        print(i)
        movieHead = movieCard.find(class_="lister-item-header")
        movieName = movieHead.find("a").text
        movieLink = movieHead.find("a").get('href')
        year = movieHead.find(class_="lister-item-year").text
        movieYear = re.search(r'(\d{4})', year).group(1)
        movieImg = movieCard.find(class_="lister-item-image").find('img').get("loadlate")
        movieDiscr = movieCard.find(class_="lister-item-content").findAll('p')[1].text
        movieDirAndStars = movieCard.find(class_="lister-item-content").findAll('p')[2].text

        try:
            movieDir = re.search(r'[\s\n]*(Directors|Director):\n((.*\n)*)\|', movieDirAndStars).group(2).strip()
        except AttributeError:
            movieDir = None

        try:
            movieStr = re.search(r'[\n\s]*(Stars|Star):\n((.*\n)*)', movieDirAndStars).group(2).strip()
        except AttributeError:
            movieStr = None

        # Write on CSV
        # writer.writerow([i, movieName, movieYear, movieLink, movieImg, movieDiscr, movieDir, movieStr])
        records.append((i, movieName, movieYear, movieLink, movieImg, movieDiscr, movieDir, movieStr))

    # Loop Continuation
    start = end+1

# Close the file
# file.close()

# Export as csv
data_frame = pd.DataFrame(records, columns=['Order No', 'Movie Name', 'Movie Year', 'Movie Content URL',
                                            'Movie Image URL', 'Movie Discription', 'Directors', 'Stars'])
data_frame.to_csv('Pandas_Data_frame.csv', index=False, encoding='utf-8')

# Confirmation
print("Scraping Finished")
