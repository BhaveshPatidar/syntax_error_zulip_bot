from goodreads import client
from typing import Optional, Any, Dict, Tuple
import bs4
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pyvirtualdisplay import Display

#Creating an instance of goodreads client

gc = client.GoodreadsClient('0Z5PqyBvGH3hnKYoLqd8qQ', 'b42ur2uhRh7Re354EBYaggqjUpAYAKrvtsKK5jj0UcQ')
commands_list = ('SearchByTitle', 'SimilarBooks', 'SearchByAuthor', 'GetDescription', 'GetPrice')


#settings for browser window opened by selenium 
display = Display(visible=0, size=(800, 600))
display.start()

option = webdriver.ChromeOptions()
option.add_argument("--disable-notifications")

capa = DesiredCapabilities.CHROME.copy()
capa["pageLoadStrategy"] = "none"
browser = webdriver.Chrome(desired_capabilities = capa, chrome_options = option)
wait = WebDriverWait(browser,240)


class GoodReadsHandler(object):
    '''
    This plugin facilitates searching GoodReads to find comprehensive 
    details of a book. It also gives a user an option to explore books by an author.
    It shows you similar books to a book entered by the user. It gives you the description 
    of the book and lastly, has the feature to give price of the book on amazon.
    '''

    def usage(self) -> str:
        return '''
           This plugin facilitates searching GoodReads to find comprehensive 
           details of a book. It also gives a user an option to explore books by an author.
           It shows you similar books to a book entered by the user. It gives you the description 
           of the book and lastly, has the feature to give price of the book on amazon.     
        '''
    help_content = "*Help for GoodReads bot* :robot_face: : \n\n" \
                   "The bot responds to messages starting with @mention-bot.\n\n" \
                   "`@mention-bot SearchByTitle <book name>` will return top related books for the given `<book name>`.\n" \
                   "`@mention-bot SimilarBooks <book name>` returns similar books to the book entered by the user.\n" \
                   "`@mention-bot GetDescription <book name>` returns book description of the given <book name>.\n" \
                   "`@mention-bot GetPrice <book name>` returns price of the top book result on amazon for the given <book name>.\n" \
                   "`@mention-bot SearchByAuthor <author name>` will return a list of books authored by given <author name>.\n \n" \
                   "Example:\n" \
                   " * @mention-bot SearchByTitle Pride and Prejudice\n" \
                   " * @mention-bot SearchByAuthor Dan Brown"

    def handle_message(self, message: Dict[str, str], bot_handler: Any) -> None:
       if message['content'] == '' or message['content'] == 'help':
            bot_handler.send_reply(message, self.help_content)
       
       else:
             cmd, query = get_command_query(message)
             print(cmd)
             
             if cmd == 'SearchByTitle':
              bot_response = get_book_by_title(query)
              bot_handler.send_reply(message, bot_response)

             elif cmd == 'SearchByAuthor':
              bot_response = get_book_by_author(query)
              bot_handler.send_reply(message, bot_response)

             elif cmd == 'GetDescription':
              bot_response = get_description_for_book(query)
              bot_handler.send_reply(message, bot_response)
             
             elif cmd == 'SimilarBooks':
              simbooks = get_similar_books(query)
              for simbook in simbooks:
                bot_response = str(simbook) + "\n"
                bot_handler.send_reply(message, bot_response)

             elif cmd == 'GetPrice':
              bot_response = get_book_price_amazon(query)
              bot_handler.send_reply(message, bot_response)

             else:
              bot_handler.send_reply(message,"Sorry, did not get that command!")


def get_command_query(message: Dict[str, str]) -> Tuple[Optional[str], str]:
    blocks = message['content'].split()
    command = blocks[0]
    
    if command in commands_list:
        query = message['content'][len(command) + 1:].lstrip()
        return command, query
    
    else:
        return None, message['content'] 

def get_book_price_amazon(query:str) -> str:
  try:
    browser.get('https://www.amazon.in/')
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#twotabsearchtextbox')))
    searchbox = browser.find_element_by_css_selector('#twotabsearchtextbox')
    searchbox.click()
    searchbox.send_keys(query)
    search = browser.find_element_by_class_name('nav-input')
    search.click()
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'a-color-price')))
    price = browser.find_element_by_class_name('a-color-price')
    browser.quit()
    display.stop()
    return price.text

  except:
    return 'There was an error executing the task. Maybe the page failed to load. Check your connection and enter the query again'
    

def get_book_by_title(query:str) -> str:
    books = gc.search_books(query)
    
    if books[0].title == '':
      error = "Sorry, couldn't find any results for that book"
      return error
    
    else:
      return prettyprint_book(books)

def get_similar_books(query:str) ->str:
    books = gc.search_books(query)
    book  = books[0]
    sim_books = book.similar_books
    
    if sim_books[0] == '':
      error = error = "Sorry, couldn't find any similar books"
      return error
    
    else:
      return sim_books 

def get_book_by_author(query:str) ->str:
    books = gc.search_books(query)
    if books[0].title == '':
      error = "Sorry, couldn't find any results for that book"
      return error
    
    else:
      return prettyprint_book(books)

def get_description_for_book(query:str) -> str:
    books = gc.search_books(query)
    return bs4.BeautifulSoup(books[0].description, 'html.parser').text.strip()
 
def prettyprint_book(books) -> str:
    bot_response = ""
    for book in books:
        print(book)
        auth = book.authors[0]
        book_list = {'Author':auth.name, 'Rating':book.average_rating, 'Title':book.title[:50] } 
        bot_response = bot_response + "\n" + "Name of book is: " + book_list['Title'] + "    written by: " + book_list['Author'] + "   and having an average rating of: " + book_list['Rating'] 
    
    return bot_response


handler_class = GoodReadsHandler
