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
Log the book names only, useful to prep filenames if using local
'''

logger = logging.getLogger(__name__)
logging.basicConfig(filename='/mnt/base-us/fixcovers.log', encoding='utf-8', level=logging.DEBUG,format='%(asctime)s %(levelname)s:%(message)s')
logger.info("Show Missing File Names started")                  
connection = sqlite3.connect("/var/local/cc.db")
cursor = connection.cursor()
rows = cursor.execute("SELECT p_titles_0_nominal, p_thumbnail, p_credits_0_name_collation  FROM Entries WHERE p_isArchived = 0 and p_contentSize > 0").fetchall()
for row in rows:
    cover_name = os.path.join("/mnt/base-us/documents",row[0].lower().replace(" ","_")+'.jpg')
    if row[1] and os.path.isfile(row[1]):
        file_size = os.path.getsize(row[1]) #12732
        if file_size<1000:                        
            logger.debug(f"{row[0]} needs a cover ({cover_name})")
    else:        
        logger.debug(f"{row[0]} needs a cover ({cover_name})")
logger.info("Show Missing File Names ended")                  

