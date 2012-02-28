#### Base URL for requests
	/api/corporations/{method}.{format}

#### Required GET paramaters
* *method:* get (for a single corporation) or getList (for list of corporations)
* *.format:* .xml or .json

#### Optional GET paramaters
* *name*
	name of this corporation(s)
* *for_profit*
	is this a for-profit corporation (i.e. 1 or 0)
* *sourcewatch_url*
	url of this corporation on sourcewatch wiki, if available
* *background_info*
	background info on this corporation's ALEC ties
* *include_citations*
	should response data include citations? (i.e. 1 or 0)
