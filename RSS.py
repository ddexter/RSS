import readFeed
import storeFeed

if __name__ == "__main__":
    rf = readFeed.ReadFeed()
    rf.login("", "")
    rf.authenticate()
    articles = rf.readStarred()
    rf.removeStars(articles)

    db = storeFeed.StoreFeed()
    db.connect("", "", "", "")
    db.insert(articles)

