#### Base URL for requests
	/api/politicians/{method}.{format}

#### Required GET paramaters
* *method:* get (for a single legislator) or getList (for multiple legislators)
* *.format:* .xml or .json

#### Optional GET paramaters
* *title*
	title of this politician(s) (i.e. 'Sen', 'Rep', 'Gov')
* *full_name*
	full name of this politician(s)
* *party*
	party of this politician(s) (i.e. 'R', 'D', 'I')
* *state*
	state of this politician (i.e. 'Massachusetts', 'Rhode Island')
* *background_info*
	background info on this politicians ALEC ties
* *NOT WORKING: os_id*
	Open States id for this politician (from the [Open States project](http://openstates.org/))
* *include_citations*
	should response data include citations? (i.e. 1 or 0)
