import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from io import StringIO
from os.path import dirname

import pymongo
from urllib.parse import quote_plus
import sys

class Crawler:
    def __init__(self):
        # Get mongo connection info from user
        uri = input("Input your MongoDB uri: ")

        # Try to connect to mongo
        try:
            client = pymongo.MongoClient(uri)
        # Return a friendly error if a URI error is thrown
        except pymongo.errors.ConfigurationError:
            print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
            sys.exit(1)

        self.db = client["zcrawler"]
        self.queue_col = self.db["queue"]
        self.visited_col = self.db["visited"]
        self.repository_col = self.db["repository"]

    def get_start(self, input):
        # Check if any documents exist in the queue
        if self.queue_col.count_documents({}, limit = 1):
            output =  self.queue_col.find_one_and_delete({}, sort={'_id': 1}).url
            print(output)
            return output
        elif input == "1":
            return "https://en.wikipedia.org/wiki/Heart"
        elif input == "2'":
            return input("Please enter a link to begin at: ")
        else:
            print("Invalid input to get_start.")
            sys.exit(1)

    def get_next(self):
        # Check if any documents exist in the queue
        if self.queue_col.count_documents({}, limit = 1):
            output =  self.queue_col.find_one_and_delete({}, sort={'_id': 1}).url
            print(output)
            return output
        else:
            print("Wasn't able to find anything in queue. Stopping.")
            sys.exit(1)

    def bfs(self, url):
        self.visited_col.insert_one( {"url": url} )
        html_text = requests.get(url).text
        doc = BeautifulSoup(html_text, 'html.parser')
        parsed_url = urlparse(url)
        
        # Handle each link in the document
        for link in doc.find_all('a'):
            l = (link.get('href'))

            if self.visited_col.find_one( {"url": url} ) is not None:
                continue

            elif (l is None or len(l) < 2):
                continue
                
            # Handle '/' links
            elif (len(l) > 1 and l[0] == '/' and l[0:2] != '//'):
                link_builder = StringIO()
                link_builder.write(parsed_url.scheme)
                link_builder.write("://")
                link_builder.write(parsed_url.hostname)
                link_builder.write(l)
                l = link_builder.getvalue()
                self.queue_col.insert_one( {"url": url} )
                print(l)
                
            # Handle '//' links
            elif (len(l) > 1 and l[0:2] == '//'):
                link_builder = StringIO()
                link_builder.write(parsed_url.scheme)
                link_builder.write(":")
                link_builder.write(l)
                l = link_builder.getvalue()
                self.queue_col.insert_one( {"url": url} )
                print(l)
                
            # Handle './' links
            elif (len(l) > 1 and l[0:2] == './'):
                link_builder = StringIO()
                link_builder.write(parsed_url.scheme)
                link_builder.write("://")
                link_builder.write(parsed_url.hostname)
                link_builder.write(dirname(parsed_url.path))
                link_builder.write(l[1:])
                l = link_builder.getvalue()
                self.queue_col.insert_one( {"url": url} )
                print(l)
                
            # Handle '#' links
            elif (l[0] == '#'):
                link_builder = StringIO()
                link_builder.write(parsed_url.scheme)
                link_builder.write("://")
                link_builder.write(parsed_url.hostname)
                link_builder.write(parsed_url.path)
                link_builder.write(l)
                l = link_builder.getvalue()
                self.queue_col.insert_one( {"url": url} )
                print(l)
                
            # Handle '../' links
            elif (len(l) > 3 and l[0:3] == '../'):
                link_builder = StringIO()
                link_builder.write(parsed_url.scheme)
                link_builder.write("://")
                link_builder.write(parsed_url.hostname)
                link_builder.write('/')
                link_builder.write(l)
                l = link_builder.getvalue()
                self.queue_col.insert_one( {"url": url} )
                print(l)
                
            # Handle 'javascript:' links
            elif (len(l) > 11 and l[0:11] == 'javacript:'):
                continue
            
            # Handle 'mailto:' links
            elif (len(l) > 7 and l[0:7] == 'mailto:'):
                continue
            
            # Handle remaining links
            elif (len(l) > 5 and l[0:5] != 'https' and l[0:4] != 'http'):
                link_builder = StringIO()
                link_builder.write(parsed_url.scheme)
                link_builder.write("://")
                link_builder.write(parsed_url.hostname)
                link_builder.write(l)
                self.queue_col.insert_one( {"url": url} )
                print(l)
