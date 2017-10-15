# Twitter Sentiment Analyzer

Twitter Sentiment Analyzer is a python project design to fetch **Live Tweets** on user given keyword and assign sentiments to those tweets. 
Tweets are classified as *Positive*, *Negative* or *Neutral* using [Naive Bayes Classifier](https://en.wikipedia.org/wiki/Naive_Bayes_classifier).

This project is tested on `Python 2.7` with *Xampp* as `PHP` working environment on *Google Chrome v50.x* and above.

Minimum Requirements:

1. Python 2.7
2. PHP 
3. Twitter Account with Login credentials like `consumer_key`, `consumer_secret,access_token` and `access_token_secret`. (Find more [How to Find your Twitter consumer key](https://stackoverflow.com/questions/1808855/getting-new-twitter-api-consumer-and-secret-keys))

# Steps to Setup Environment:

1. Clone the project on your system.
2. Place your Twitter credentials in **config.json**.
3. Place **search_result.php** file in your `htdocs` folder of php installation directory(like `Xampp`).
4. Place appropriate path of your this project in search_result.php at *line no 3* in `$url`.

# Steps to Run the Project:

1. Start the Xampp Server
2. Open *cmd console* or *terminal* in current Directory and start the Python Server as: 
	>`python -m CGIHTTPServer 9002` (9002 is a Port number, you can specify any).
3. Open any Web Browser, and head to `localhost:9002` (or the port you used in Step 1)
4. Click the Start button.
5. Enter the keyword to search for like *Watson*.
6. You will be able to visualize the results.