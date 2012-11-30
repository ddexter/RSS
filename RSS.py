import dbConnector
import readFeed
import storeFeed
import storeWord

if __name__ == "__main__":
    db = dbConnector.DBConnector()
    conn = db.connect("", "", "", "")

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

