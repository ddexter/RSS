import createFeed
import dbConnector
import ftp
import readFeed
import storeFeed
import storeWord
import sys
import tagCloud

if __name__ == "__main__":
    db = dbConnector.DBConnector()
    conn = db.connect("", "", "", "")
    
    if conn == None:
        sys.exit()

    # Read feeds from starred items in Google Reader (this deletes starred)
    rf = readFeed.ReadFeed()
    rf.login("", "")
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
    tagCloud.makeCloud(tagsCounts)

    # Create personal RSS feed
    articles = feedStore.getArticles()
    myFeed = createFeed.CreateFeed()
    rss = myFeed.createRSSXML(articles)

    # Push tag cloud and RSS feed to server
    server = ftp.FTP()
    server.connect("", "", "" , "")
    server.push("", "")
    server.push("", "")
    server.close()

