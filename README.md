# Basic Git Scraper Template

I changed the code to scrap the author of the most recent crossword and time of when the crossword was published. 

I, first, made a request to the Crosswords page to get the URL of the latest crossword.
Then, make a request to the URL of the latest crossword to get the author and time of the crossword. I used beautifulSoup and .get() to help me parse the HTML data in order to extract the neccesary data.


## Additional Note
"As of May 1st, the DP no longer has any new crosswords, and therefore no new puzzles are being scraped at this time being." 
"Also, the cache error prevented me some scraping towards the middle and end of april."
