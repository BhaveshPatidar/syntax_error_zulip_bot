# Project Title

Zulip Chatbot plugin which facilitates searching GoodReads to find comprehensive 
details of a book. It also gives a user an option to explore books by an author.
It shows you similar books to a book entered by the user. It gives you the description 
of the book and lastly, has the feature to give price of the book on amazon.

## Getting Started

Follow the instructions on https://chat.zulip.org/api/running-bots to run the bot on your system. 

## Using the bot
"*Help for GoodReads bot* :robot_face: : \n\n" \
                   "The bot responds to messages starting with @mention-bot.\n\n" \
                   "`@mention-bot SearchByTitle <book name>` will return top related books for the given `<book name>`.\n" \
                   "`@mention-bot SimilarBooks <book name>` returns similar books to the book entered by the user.\n" \
                   "`@mention-bot GetDescription <book name>` returns book description of the given <book name>.\n" \
                   "`@mention-bot GetPrice <book name>` returns price of the top book result on amazon for the given <book name>.\n" \
                   "`@mention-bot SearchByAuthor <author name>` will return a list of books authored by given <author name>.\n \n" \
                   "Example:\n" \
                   " * @mention-bot SearchByTitle Pride and Prejudice\n" \
                   " * @mention-bot SearchByAuthor Dan Brown"

### Prerequisites

Some third-party modules need to be downloaded to run some of the scripts. 

```
Selenium
Latest Chrome Driver
goodreads
bs4 ( Beautiful Soup) 
pyvirtualdisplay

```
You also need to have your own API key for Goodreads from : https://www.goodreads.com/api/keys

## Built With

* Python 2.7.15

## Authors

* **Bhavesh Patidar** - [BhaveshPatidar](https://github.com/BhaveshPatidar)
* **Srijan Dubey** 

