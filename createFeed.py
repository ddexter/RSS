import BeautifulSoup
import consts
import time

from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, Comment
from xml.dom import minidom

class CreateFeed:
    def prettifyRSS(self, rssXML):
        roughStr = ElementTree.tostring(rssXML, "utf-8")
        reparsed = minidom.parseString(roughStr)
        
        return reparsed.toprettyxml(indent="  ")

    def stripHTML(self, string):
        # Get rid of all html tag and interior content
        txt = BeautifulSoup.BeautifulSoup(string).findAll(text=True)

        if txt != None:
            return ''.join(txt)
        else:
            return ''

    def createRSSXML(self, articles, fileName="rss.xml", feedTitle = '',\
        feedLink = '', feedDescription= ''):

        # Open file
        out = open(fileName, "w")

        # Create the RSS XML object
        rss = Element("rss")
        rss.set("version", "2.0")

        channel = SubElement(rss, "channel")

        title = SubElement(channel, "title")
        title.text = feedTitle

        link = SubElement(channel, "link")
        link.text = feedLink

        description = SubElement(channel, "description")
        description.text = feedDescription

        # Print XML for items
        for article in articles:
            item = SubElement(channel, "item")

            guid = SubElement(item, "guid")
            guid.text = str(article[0]).decode("utf-8")

            title = SubElement(item, "title")
            title.text = self.stripHTML(str(article[1]).decode("utf-8"))

            description = SubElement(item, "description")
            desc = self.stripHTML(str(article[2]).decode("utf-8"))
            if len(desc) > 140:
                description.text = desc[0:141]
            else:
                description.text = desc

            link = SubElement(item, "link")
            link.text = str(article[3]).decode("utf-8")

            pubDate = SubElement(item, "pubDate")
            pubDate.text = str(article[4]).decode("utf-8")

        rss = self.prettifyRSS(rss)

        out.write(rss.encode("utf-8"))
        out.close()
