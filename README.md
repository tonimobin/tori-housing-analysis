## Interactive web application for visualizing housing data scraped from [Tori.fi](https://www.tori.fi/koko_suomi/asunnot/myytavat_asunnot?ca=18&cg=1010&c=1012&w=3&o=1).

The objective of this app is to provide an interactive way to visualize housing data scraped of Tori.fi. The scraping is done with the aid of [Beautiful Soup](https://pypi.org/project/beautifulsoup4/) and the script can be found [here](scrape.py). The script goes over the housing listings and saves basic data of the listings based on the title ('Title', 'Rooms', 'Price', 'Size', 'Type', 'Year' and 'Location') to a .csv file [housing.csv](housing.csv). 

The web application that provides the interactive visualization is built with [Dash](https://dash.plotly.com/). The raw data from [housing.csv](housing.csv) is too incomplete so it needs further cleansing in order to be usable by the Dash components (sliders, dropdowns and so on). The cleaning in this case was done with both [Tableau Prep](https://www.tableau.com/learn/get-started/prep) and Python, which resulted in the file [full_data_cleaned_and_outliers_removed.csv](full_data_cleaned_and_outliers_removed.csv). You could visualize any data with this app, if it follows the format of this file. 

The app itself provides different ways to query the data and then proceeds to visualize the data in various ways, based on the query options made by the user. This project was done for the course [Interactive Data Visualization](https://studies.helsinki.fi/courses/cur/hy-opt-cur-2122-f77f1644-2bfe-4693-a6bb-47596553c0c4/Interactive_Data_Visualization_Lectures). 

## Gif of the app in-use
![housing-analysis](https://user-images.githubusercontent.com/85210617/167390969-c4a8d2ab-df81-410d-af7d-ded25622e28c.gif)

## Example output of the parsing file (.csv file viewed in Excel)
![Screenshot 2022-04-06 at 16 12 48](https://user-images.githubusercontent.com/85210617/161983100-c5adeb40-892b-497b-bdd6-fb90cf678d3c.png)

## Ideas for improvement
- The app runs slow on Heroku, which is partly because of Heroku's limited resources but also because of inefficient structures within the app. These structures could have been made more efficient, i.e. pre-processing data (more) outside the app, making 
- Make the code more modular. Most of the functionality is stuffed in the same [aoo.py](app.py) file. 
- The [Leaflet](https://leafletjs.com/) based map isn't as interactive as it could & should be, there's plenty of room for improvement (course deadline arrived earlier than the understanding of how to use Leaflet properly 🙂)

## Learned during development
- Better understanding of the combination of numpy, pandas and python itself in order to manipulate and wrangle data to a format that suits your needs.
- Utilizing Dash & Plotly to create visualization focused web apps. Before this project I had no idea how to approach the inclusion of visualizations within a web app, but now I've got a good basic understanding of what is required.
- Basics of web scraping, what is it based on and the challenges associated.
- Lots of minor things i.e. more in-depth understanding of CSS grid & flex and how to utilize them in order to build structure for your web application, using [LottieFiles](https://lottiefiles.com/) for the first time in order to use small animations on the site,   
- 
## Could have done differently
- I deployed the app to Heroku very last minute and it is here where I noticed that the app actually runs very slow compared to running locally. I suppose the deployment should've been done early on, because I could've then tried to optimize the performance during development.
-  A better planning process. I was very keen on starting the development right away, because I felt like I wanted to start learning Dash right away. I do feel like I could've benefitted from doing a more in-depth plan before starting the actual code development.
-  From the viewpoint of this being a course project, I feel like the decision to 'create my own dataset' was neat, but it did come at the cost of my data being a bit boring. What I mean by this is that the dataset that I created by parsing Tori.fi didn't really allow me to build any advanced visualizations, i.e. animated graphs and most of the visualizations that I did end up making are fairly plain and could've been achieved with very small effort in Excel for example. So the data could've been a bit more complex, which would've allowed me to build a bit more complex visualizations. 
## Useful material
- [Python Web scraping to CSV file| BeautifulSoup | Real Estate Website Scraping](https://www.youtube.com/watch?v=RvCBzhhydNk).
- [Beautiful Soup Tutorial 2. – How to Scrape Multiple Web Pages](https://data36.com/scrape-multiple-web-pages-beautiful-soup-tutorial/)
- [Plotly Dash Complete Tutorial](https://www.youtube.com/playlist?list=PLH6mU1kedUy8fCzkTTJlwsf2EnV_UvOV-)
- [Charming Data's playlists on YouTube](https://www.youtube.com/c/CharmingData/playlists)
- [Map Visualizations with Dash Leaflet - Haw-minn Lu | PyData Global 2021](https://www.youtube.com/watch?v=OVggxyO81CQ)
