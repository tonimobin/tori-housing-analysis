## Housing listings data analysis & visualization (Work in progress)

Tiny script to practise data scraping in a 'real scenario'. The script goes over housing listings that are being offered for sale at Tori.fi. Once basic data of the listings are retrieved, they are saved to a .csv file. The url that is being scraped can be accessed [here](https://www.tori.fi/koko_suomi/asunnot/myytavat_asunnot?ca=18&cg=1010&c=1012&w=3&o=1). An interactive visualization based on the scraped data is under construction!

## Running the script

1. `pip3 install -r requirements.txt`
2. `python3 scrape.py`
3. (Temporary): Multi-page results are appended to the existing housing.csv, so delete the existing file if you want completely fresh results.
4. (Display Dash data-app): `python3 app.py` and go to url `http://localhost:8050/`, incase Dash module can't be found try: `python3 -m pip install dash`

## Example output of the parsing file (.csv file viewed in Excel)
![Screenshot 2022-04-06 at 16 12 48](https://user-images.githubusercontent.com/85210617/161983100-c5adeb40-892b-497b-bdd6-fb90cf678d3c.png)

## Screenshots of the Dash app (WIP)

## Functionality of the script

1. Go to Tori.fi, look at houses being offered for sale.
2. Find the relevant html elements for 'Title', 'Rooms', 'Price', 'Size', 'Type', 'Year' and 'Location'.
3. Format the results to .csv and save to file `housing.csv`

## Ideas for improvement

- ~~More precise validation (i.e. remove records without pricing information)~~
    - ~~Explicit form for every record~~ (Done for the Dash app, drops rows with missing columns)
    - Option to remove records with missing info (the one's not fulfilling the requirements of the explicit form)
- ~~More fields, more scraped data~~
    - ~~The title often contains useful info, maybe try to parse it somehow and extract keywords~~
    - ~~Year~~
- ~~Go through more than 1 page of results, maybe all of the results?~~
    - Support for scraping the first x pages could be useful, possibly scrape by date of listing as well?
- Make this into a proper project, create a frontend for the results and integrate some analysis & visualization based on the scraped results (possibly scrape more sites such as Oikotie & Vuokraovi and aggregate the results)
- Create a small data app with [Dash](https://dash.plotly.com/)? (WIP)
    - Heat map / Bubble map for number of listings by location
    - Key figures panel for displaying values such as average cost of m<sup>2</sup> in €, average construction year and so on (corresponding to the selections in the Dash app)
    - 2-4 other visualizations (which are the most relevant / interesting ones?)

## Useful material

- [Python Web scraping to CSV file| BeautifulSoup | Real Estate Website Scraping](https://www.youtube.com/watch?v=RvCBzhhydNk).
- [Beautiful Soup Tutorial 2. – How to Scrape Multiple Web Pages](https://data36.com/scrape-multiple-web-pages-beautiful-soup-tutorial/)
- [Plotly Dash Complete Tutorial](https://www.youtube.com/playlist?list=PLH6mU1kedUy8fCzkTTJlwsf2EnV_UvOV-)
- [Charming Data's playlists on YouTube](https://www.youtube.com/c/CharmingData/playlists)
