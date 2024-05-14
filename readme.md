Workflow:
Note: We should probably scrape the english version! LLMs are better at English.

1. Get the hotels from random dates. Get their name + link.
    - The link includes a date, but that does not matter much. From this page, we can get general info regarding the hotel
    - The price of course varies by date. If they are to implement this, they would have this data. We can probably get some sample data regarding this, by scraping different dates, to illustrate the idea.
    
2. Get the individual hotel data. Supplement and add regarding rating, the amount of reviews, location etc. 
    - Can use the description as well, since LLMs can actually use long descriptions as well, to get a better understanding for example:
    "Det stilfulde Hotel Alexandra ligger 200 m fra Københavns Rådhusplads og Tivoli. De lydisolerede værelser har aircondition, fladskærms-tv, te- og kaffemaskine samt klassiske danske designermøbler. Der er gratis wi-fi i Alexandras lobby og på alle værelserne. Hotel Alexandra er et miljøvenligt hotel."

3. (Optional): With the address being found, we can use maps to get long/lat. This way we make something to calculate distance.