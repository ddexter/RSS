import psycopg2
import time

from datetime import datetime

class StoreFeed:
    def __init__(self):
        self._TABLE = "rssfeed"
        self._conn = None

    def connect(self, host, dbname, user, password):
        # Connect to database
        self._conn = None
        try:
            connStr = "host='%s' dbname='%s' user='%s' password='%s'" % (host, dbname, user, password)
            self._conn = psycopg2.connect(connStr)
        except:
            print("Unable to connect")

        # Create table if it does not exist
        cursor = self._conn.cursor()
        existsStr = "SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name='rssfeed')"
        cursor.execute(existsStr)

        if not cursor.fetchone()[0]:
            createStr = "CREATE TABLE rssfeed(id SERIAL PRIMARY KEY, title VARCHAR(512) NOT NULL, description TEXT NOT NULL, link VARCHAR(512) NOT NULL, pubDate DATE NOT NULL)"
            cursor.execute(createStr)
            self._conn.commit()

    def insert(self, articles):
        cursor = self._conn.cursor()
        rows = []
        for article in articles:
            # convert Unix Epoch (seconds) to datetime
            rows.append({"title":article["title"],\
                "description":article["summary"]["content"],\
                "link":article["alternate"][0]["href"],\
                "pubDate":article["published"]})

        insertStr = """INSERT INTO rssfeed(title, description, link, pubDate) VALUES (%(title)s, %(description)s, %(link)s, to_timestamp(%(pubDate)s))"""
        cursor.executemany(insertStr, rows)
        self._conn.commit()

