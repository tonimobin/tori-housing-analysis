## Miniscript for scraping Tori.fi housing data (Work in progress)

Tiny script to practise data scraping in a 'real scenario'. The script goes over housing listings that are being offered for sale at Tori.fi. Once basic data of the listings are retrieved (title, price, location), they are saved to a .csv file. The url that is being scraped can be accessed [here](https://www.tori.fi/koko_suomi/asunnot/myytavat_asunnot?ca=18&cg=1010&c=1012&w=3&o=1).

## Running the script

1. `pip install -r requirements.txt`
2. `python3 scrape.py`
3. (Temporary): Multi-page results are appended to the existing housing.csv, so delete the existing file if you want completely fresh results.

## Example output (.csv file viewed in Excel)
![Screenshot 2022-03-27 155238](https://user-images.githubusercontent.com/85210617/160282329-31d99f00-9f09-4339-a1ad-2010be32bb60.png)

## Functionality of the script

1. Go to Tori.fi, look at houses being offered for sale.
2. Find the relevant html elements for 'Title', 'Price (€/mo)' and 'Location'.
4. Format the results to .csv and save to file `housing.csv`

## Ideas for improvement

- More precise validation (i.e. remove records without pricing information)
    - Explicit form for every record
    - Option to remove records with missing info (the one's not fulfilling the requirements of the explicit form)
- More fields, more scraped data
    - Date of listing
    - The title often contains useful info, maybe try to parse it somehow and extract keywords
    - Year 
- Go through more than 1 page of results, maybe all of the results? (WIP)
    - Basic functionality done as of 1st APR, but the script is rather slow.
    - Scraping all of the results leads to 10000 records.
    - Support for scraping the first x pages could be useful, possibly scrape by date of listing as well?
- Make this into a proper project, create a frontend for the results and integrate some analysis & visualization based on the scraped results (possibly scrape more sites such as Oikotie & Vuokraovi and aggregate the results)
    - Create a small data app with [Dash](https://dash.plotly.com/)?

## Useful material

- [Python Web scraping to CSV file| BeautifulSoup | Real Estate Website Scraping](https://www.youtube.com/watch?v=RvCBzhhydNk).
- [Beautiful Soup Tutorial 2. – How to Scrape Multiple Web Pages](https://data36.com/scrape-multiple-web-pages-beautiful-soup-tutorial/)