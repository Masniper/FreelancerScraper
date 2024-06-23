# Freelancer(.com) Scraper

This project scrapes the jobs page from Freelancer.com for a given link and sends alerts for each job via Telegram. It also continuously checks for new jobs at regular intervals.

### About the Project

- Sends all job alerts to Telegram via bot.
- Built with requests and BeautifulSoup libraries.

### Usage

1. Choose skills you are interested in from [this link](https://www.freelancer.com/jobs/django_web-scraping_python_data-mining_microsoft-sql-server_tsql/?languages=en) and update the `CATEGORIES` variable in `main.py`.
2. Create a Telegram bot and obtain the bot token.
3. Obtain the chat ID where you want to send the alerts.
4. Create a `.env` file in the project root directory and add your `TELEGRAM_TOKEN` and `CHAT_ID` in the following format:
5. Install the required dependencies:
```sh
$ pip install -r requirements.txt
```
### Installation
If you want to contribute to the project or update dependencies, don't forget to add docstrings and update requirements.txt accordingly using:
```sh
$ pip freeze > requirements.txt
```
### Running the Project
Activate your virtual environment:
```sh
$ source venv/bin/activate   # For Linux and macOS
$ venv\Scripts\activate      # For Windows
```
Then run the main script:
```sh
$ python main.py
```
### License
This repository is licensed under the MIT License. Please see the LICENSE file for more details.
