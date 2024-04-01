from scraping.scraper import ScrapeWithDriver
from db.db_setup import dbConnection
from app.flask import app_creation


flats_scraper = ScrapeWithDriver()
scraped_data = flats_scraper.scrape()

db = dbConnection()
db.execute("DROP TABLE IF EXISTS flats;")
db.commit()
db.execute("CREATE TABLE flats (id SERIAL PRIMARY KEY, title VARCHAR NOT NULL, img_address VARCHAR NOT NULL) ")
db.commit()

statement = """INSERT INTO flats (title, img_address) VALUES (%s, %s)"""
for d in scraped_data:
    d['img_address'] = ' '.join(d['img_address'])

for line in scraped_data:
    try:
        print(statement, (line['title'], line['img_address']))
        db.execute(statement, (line['title'], line['img_address']))
    except Exception as error:
        print('Error! ', error)
db.commit()
db.close()


app_creation()