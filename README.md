## Miniscript for scraping Tori.fi housing data

Tiny script to practise data scraping in a 'real scenario'. The script just goes over the first page of apartments that are being offered for renting at Tori.fi, the url that is being scraped can be accessed [here](https://www.tori.fi/uusimaa?q=&cg=1010&w=3&st=u&c=1014&ros=&roe=&ss=&se=&ht=&at=&mre=&ca=18&l=0&md=th).

## Running the script

1. `pip install -r requirements`
2. `python3 scrape.py`

## Example output

## Functionality of the script

1. Go to Tori.fi, look at apartments being offered for rental (Only page 1).
2. Find the relevant html elements for 'Title', 'Price (€/mo)' and 'Location'.
3. Save the findings to a .csv file

## Ideas for improvement

- More precise validation (i.e. remove records without pricing information)
- More fields, more scraped data
- Go through more than 1 page of results, maybe all of the results?
- Make this into a proper project, create a frontend for the results and ingrate some analysis & visualization based on the scraped results (possibly scrape more sites such as Oikotie and Vuokraovi)

## Misc.

The code is based on a tutorial, which can be found [here](https://www.youtube.com/watch?v=RvCBzhhydNk).