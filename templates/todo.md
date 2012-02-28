#### To Do:

##### Not working...
* Fix regex to parse legislator data
* Fix search to open states (need to check former & current legislators)

##### To Scrape
* State chairmen politicians
* award winning people & politicians
* task force information

##### Data to clean up
* legislators.background_info -- remove surrounding tags
* convert state names to 2 character shortcodes
* move some text from corporations.name corporations.background_info
* model_bills.text (pdf text conversion) is very bad -- use regex and more

#### Completed
* Scraping for-profit corporations
* Scraping non-profit corporations
* Added model_bills to database with automated pdf to text 
* JSON & XML generation for data in any database table
* above used for url query based api
* user registration w/ unique api key 
