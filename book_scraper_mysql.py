import mysql.connector
import requests
from bs4 import BeautifulSoup

connection = mysql.connector.connect(
    host='localhost',
    user='your_mysql_user',
    passwd='your_mysql_ps',
    database='books'
)
c = connection.cursor()


def scrape_books(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article")
    all_books = []
    for book in books:
        book_data = (get_price(book), get_title(book), get_ratings(book))
        all_books.append(book_data)
    # print(all_books)
    save_book(all_books)

def save_book(all_books):
# COMMENT OUT DROP, CREATE DATABASE AND CREATE TABLE AFTER RUNNING THE FILE THE FIRST TIME
    c.execute("DROP books")
    c.execute("CREATE DATABASE books")
    c.execute("CREATE TABLE books (price REAL, title TEXT, rating REAL)")
    c.executemany("INSERT INTO books VALUES(%s, %s, %s)", all_books)
    connection.commit()
    connection.close()


    
def get_title(book):
    title = book.find("h3").find("a")["title"]
    return title    

def get_price(book):
    price = book.select(".price_color")[0].get_text()
    price = float(price.replace("Â", "").replace("£", ""))
    return price

def get_ratings(book):
    ratings = {"Zero": 0, "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    paragraph = book.select(".star-rating")[0]
    rating = paragraph.get_attribute_list("class")[1]
    word = ratings[rating]
    return word


scrape_books("http://books.toscrape.com/catalogue/category/books/history_32/index.html")