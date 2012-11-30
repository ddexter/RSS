import psycopg2
import time

from datetime import datetime

class StoreFeed:
    def __init__(self, conn):
        self._TABLE = "rssfeed"

        if conn == None:
            return

        self._conn = conn

        # Create table if it does not exist
        cursor = self._conn.cursor()
        existsStr = "SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name='rssfeed')"
        cursor.execute(existsStr)

        if not cursor.fetchone()[0]:
            createStr = "CREATE TABLE rssfeed(id SERIAL PRIMARY KEY, title VARCHAR(512) NOT NULL, description TEXT NOT NULL, link VARCHAR(512) NOT NULL, pubDate DATE NOT NULL)"
            createIdxStr = "CREATE INDEX date_idx ON rssfeed(pubDate)"
            cursor.execute(createStr)
            cursor.execute(createIdxStr)
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

