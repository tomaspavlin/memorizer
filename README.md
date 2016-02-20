# Installation
1. Run http server

	```python
	./server.py
	```
2. Make sure there are 3 files named *to_upload*, *scheduler_data* and *new* in *data* directory.
	```
	data/
		|--	to_upload
		|--	scheduler_data
		|--	new
	```

	Make sure that the *data/scheduler_data* file contains at least following line.
	```
	[]
	```

3. Plan scheduler and uploader to run every day. For example add this line into crontab:

	```
	0	4	*	*	*	<path_to_this_dir>/day_routine.sh >> <path_to_this_dir>/day_routine.log 2>&1
	```

4. Install *chrome extension*



# Architecture overview
```
utils.py	- some handy functions
conf.json	- configuration of py files
get_quizlet_access_token.php	- script for obtaining access token thats written in config file

chrome-extension	->	server.py 	->	data/new - add new keyword here
									->	quizlet.py	->	recreate new set

cron	->	day_routine.sh
				|
				|--->	saves output to day_routine.log
				|--->	backup data using tar
				|--->	scheduler.py status	- prints data in scheduler_data
				|
				|		data/new
				|			|
				|			|
				|--->	scheduler.py	<->	data/scheduler_data
				|						-->	data/to_upload
				|
				|--->	uploader.py		<--	data/to_upload
										-->	quizlet.py	--> create daily set
														--> remove new set 

```

# Usage
## Chrome extension
This extension will **inject** it's icons into *slovnik.cz*. If you click these icons, the word pair will be added into your wordlist.

You can click the extension **icon in the top of the chrome** and you well be able to add your own pair into wordlist.

It is good idea to **configure search engines** in chrome for fast searching in slovnik.cz.