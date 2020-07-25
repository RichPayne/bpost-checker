#Monitor the status of your bpost parcel
A cli tool that enables a user to get alerts when the status of their parcel changes without having to constantly monitor the website. You are also able to recieve email alerts.

The idea behind this was inspired by the Tomorrowland bracelets, every year people spend time refreshing the bpost website to see where their bracelets are... now - they won't have to.  Simply provide your tracking ID and postal address.
##Usage
Requires chrome to work, download the correct version chrome driver for your installed version from `https://chromedriver.chromium.org/downloads` and place it in the same directory as the python script.

Install python libraries using `pip install -r requirements.txt` and then run `./bpost_checker.py <parcel id> <postal address> [email] [application password]`


