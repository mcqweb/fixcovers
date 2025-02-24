import sqlite3
import requests
import warnings
import os
import shutil
import logging

warnings.filterwarnings("ignore")

'''
Load Kindle Library
Find books
Check cover is large enough to be a real cover
Check if there is a cover at all
Look for a local cover with the filename all in lower case and _ instead of spaces
Use Local Cover
If no local cover download one
'''

logger = logging.getLogger(__name__)
logging.basicConfig(filename='/mnt/base-us/fixcovers.log', encoding='utf-8', level=logging.DEBUG,format='%(asctime)s %(levelname)s:%(message)s')

logger.info("Fix Missing Covers Started")                  
def download_cover(book,file_name):
    logger.debug(book)
    title = book[0]
    author = book[2]
    book_search = requests.get(f"https://openlibrary.org/search.json?title={title}&author={author}",verify=False).json()
    for book in book_search['docs']:
        if 'cover_i' in book:
            logger.debug(f"Downloading cover {file_name}")
            cover = requests.get(f"https://covers.openlibrary.org/b/id/{book['cover_i']}-M.jpg")
            logger.debug(cover)
            with open(file_name, mode="wb") as file:
                file.write(cover.content)
                
def fix_cover(book):
    file_name = os.path.join("/mnt/base-us/documents",book[0].lower().replace(" ","_")+'.jpg')
    if not os.path.isfile(file_name):
        #Download the cover
        download_cover(book,file_name)
    else:
        logger.debug(f"Using local cover {file_name}")
    
    if os.path.isfile(file_name):    
        os.remove(book[1])
        shutil.copy(file_name,book[1])
        logger.debug(f"{book[0]} cover added")
    else:
        logger.debug(f"No Cover available for {book[0]}")
        
def add_cover(book):
    file_name = os.path.join("/mnt/base-us/documents",book[0].lower().replace(" ","_")+'.jpg')
    new_file_name = os.path.join("/mnt/us/system/thumbnails",book[0].lower().replace(" ","_")+'.jpg')
    if not os.path.isfile(file_name):
        #Download the cover
        download_cover(book,file_name)
    else:
        logger.debug(f"Using local cover {file_name}")
    if os.path.isfile(file_name):
        shutil.copy(file_name,new_file_name)
        logger.debug(f"{book[0]} cover added")
        connection = sqlite3.connect("/var/local/cc.db")
        cursor = connection.cursor()
        rows = cursor.execute("UPDATE Entries SET p_thumbnail = '"+new_file_name+"' WHERE p_titles_0_nominal = '"+book[0]+"'")
        connection.commit() 
        connection.close() 
    else:
        logger.debug(f"No Cover available for {book[0]}")
    
connection = sqlite3.connect("/var/local/cc.db")
cursor = connection.cursor()
rows = cursor.execute("SELECT p_titles_0_nominal, p_thumbnail, p_credits_0_name_collation  FROM Entries WHERE p_isArchived = 0 and p_contentSize > 0").fetchall()
for row in rows:
    logger.debug(f"{row[0]} --> {row[1]}")
    if row[1] and os.path.isfile(row[1]):
        file_size = os.path.getsize(row[1]) #12732
        if file_size<1000:
            fix_cover(row)
    else:
        add_cover(row)


logger.info("Fix Missing Covers Ended")   