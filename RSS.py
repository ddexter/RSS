import createFeed
import dbConnector
import ftp
import readFeed
import storeFeed
import storeWord
import sys
import tagCloud

from ConfigParser import SafeConfigParser

if __name__ == "__main__":
    config = SafeConfigParser()
    config.read('/home/ddexter/projects/RSS/RSS.ini')

    GOOGLE_USER = config.get('Google', 'USER')
    GOOGLE_PASSWORD = config.get('Google', 'PASSWORD')

    DATABASE_HOST = config.get('Database', 'HOST')
    DATABASE_DB = config.get('Database', 'DB')
    DATABASE_USER = config.get('Database', 'USER')
    DATABASE_PASSWORD = config.get('Database', 'PASSWORD')

    LOCAL_RSS = config.get('Local', 'RSS')
    LOCAL_TC = config.get('Local', 'TC')

    REMOTE_HOST = config.get('Remote', 'HOST')
    REMOTE_PORT = int(config.get('Remote', 'PORT'))
    REMOTE_USER = config.get('Remote', 'USER')
    REMOTE_PASSWORD = config.get('Remote', 'PASSWORD')
    REMOTE_RSS = config.get('Remote', 'RSS')
    REMOTE_TC = config.get('Remote', 'TC')

    db = dbConnector.DBConnector()
    conn = db.connect(DATABASE_HOST, DATABASE_DB, DATABASE_USER, DATABASE_PASSWORD)
    if conn == None:
        sys.exit()

    # Read feeds from starred items in Google Reader (this deletes starred)
    rf = readFeed.ReadFeed()
    rf.login(GOOGLE_USER, GOOGLE_PASSWORD)
    rf.authenticate()
    articles = rf.readStarred()
    rf.removeStars(articles)

    # Store articles for RSS
    feedStore = storeFeed.StoreFeed(conn)
    feedStore.insert(articles)

    # Store word counts
    wordStore = storeWord.StoreWord(conn)
    wordStore.insert(articles)

    # Make word cloud
    tagsCounts = wordStore.getTopHits()
    tagCloud = tagCloud.TagCloud()
    tagCloud.makeCloud(tagsCounts, name=LOCAL_TC)

    # Create personal RSS feed
    articles = feedStore.getArticles()
    myFeed = createFeed.CreateFeed()
    rss = myFeed.createRSSXML(articles, fileName=LOCAL_RSS)

    # Push tag cloud and RSS feed to server
    server = ftp.FTP()
    server.connect(REMOTE_HOST, REMOTE_PORT, REMOTE_USER , REMOTE_PASSWORD)
    server.push(LOCAL_RSS, REMOTE_RSS)
    server.push(LOCAL_TC, REMOTE_TC)
    server.close()

