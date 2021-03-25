
# About
The backend for the Parking Lot Band project

Built with Flask and Magenta

## Resources & REST API table
| URL/ENDPOINT              | VERB   | DESCRIPTION                           |
|---------------------------|--------|---------------------------------------|
| /generateTrack/           | POST   | Returns an extended track             |

## Sample POST request contents
```
{
	"isFile": false, 
	"temperature": 1.0,
	"notes": [
		{
			"pitch": 36, 
			"start_time": 0, 
		 	"end_time": 0.125
		},
		{
			"pitch": 36, 
			"start_time": 0, 
		 	"end_time": 0.125
		}
	]
}
```

## Instructions
* Clone the repository 
* Download `basic_rnn` from [this link](https://github.com/magenta/magenta/tree/master/magenta/models/melody_rnn) (underneath "Pre-trained"), and place it under `assets/basic_rnn.mag`
* Run `pip install -r requirements.txt` to install the required libraries
* Run `python app.py` to start the server on port 3000

