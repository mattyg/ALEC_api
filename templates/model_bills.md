#### Base URL for requests
	/api/model_bills/{method}.{format}

#### Required GET paramaters
* *method:* get (for a single bill) or getList (for list of bills)
* *.format:* .xml or .json

#### Optional GET paramaters
* *name*
	name of the bill(s)
* *filename*
	filename of bill in pdf format, files are located at /static/bills/{filename} 
* *text*
	bill(s) in text format, they are poorly decoded so you ought to use the pdf's
* *NOT WORKING year_passed*
	year this bill was pass by ALEC, -1 if bill was not passed
* *NOT WORKING year_introduced*
	year this bill was introduced
