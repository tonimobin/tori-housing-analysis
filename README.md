## Miniscript for scraping Tori.fi housing data

Tiny script to practise data scraping in a 'real scenario'. The script just goes over the first page of apartments that are being offered for renting at Tori.fi, the url that is being scraped can be accessed [here](https://www.tori.fi/uusimaa?q=&cg=1010&w=3&st=u&c=1014&ros=&roe=&ss=&se=&ht=&at=&mre=&ca=18&l=0&md=th).

## 

## Functionality of the script

1. Go to Tori.fi, look at apartments being offered for rental (Only page 1).
2. Find the relevant html elements for 'Title', 'Price (€/mo)' and 'Location'.
3. Save the findings to a .csv file.

## Misc.

The code is based on a tutorial, which can be found [here](https://www.youtube.com/watch?v=RvCBzhhydNk).