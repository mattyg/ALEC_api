#### Warning: Experimental!
* This service is still in active development and is not production ready, see [features to add](/docs/todo)
* Data is licensed under [http://creativecommons.org/licenses/by-sa/3.0/](http://creativecommons.org/licenses/by-sa/3.0/) thanks to [the Center for Media and Democracy](http://www.prwatch.org/cmd)

#### API Key
You need a unique API Key, get one [here](/register)

#### Base URL for requests
	/api/{api}/{method}.{format}

#### URL paramaters
* *api:* [politicians](/docs/politicians), [corporations](/docs/corporations), [model_bills](/docs/model_bills), [task_forces](/docs/task_forces)
* *method:* get (for a single item) or getList (for multiple items)
* *.format:* .xml or .json

#### Required GET paramaters
* *apikey*
	Your personal API Key (get one [here](/register))


#### Responses

##### Error Codes
* *0* Invalid URL paramaters
* *1* No results returned
* *2* More than 1 result returned using get function, use getList instead

