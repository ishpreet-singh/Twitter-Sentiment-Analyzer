# Twitter Sentiment Analyzer

Description:

The aim of the project was to fetch tweets on user given keyword and assign sentiment to those tweets. 
Tweets are classified as Positive, Negative or Neutral using Naive Bayes Classifier.

This project is tested on Python 2.7 with Xampp as PHP working environment on Google Chrome v50.x and above.

Minimum Requirements:

1. Python 2.7
2. PHP 
3. Twitter Login credentials(consumer_key,consumer_secret,access_token,access_token_secret)

Steps to Setup Environment:

1. Clone the project on your system.
2. Place your appropriate Twitter credentials in config.json.
3. Place search_result.php file in your htdocs folder of php installation directory(like Xampp).
4. Place appropriate path of your this project in search_result.php at line number 4.

Steps to run the Project:

5. Open cmd console in current dir. and execute the program with following command: 
	python -m HTTPCGIServer 9002 (You can specify any Port number).

6. Open any Web Browser, type localhost:Port Number (eg: 9002. Same as in step 5)
7. Click start button.
8. Enter the keyword to search for.
9. Results will be displayed in Web Browser itself.