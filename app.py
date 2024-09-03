import link_handler
import mongo_wrapper

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import sys
from tqdm import tqdm

class Crawler:
    def __init__(self):
        self.client_wrapper = mongo_wrapper.MongoWrapper()
        self.link_fixer = link_handler.LinkHandler()
        self.domain = None

    def start(self, input):
        if input == "1":
            start = "https://owenzeller.com"
            if self.client_wrapper.visited_col.find_one( {"url": start} ) is None and self.client_wrapper.queue_col.find_one( {"url": start} ) is None:
                self.client_wrapper.queue_col.insert_one( {"url": start} )
            self.bfs(self.get_next())
        elif input == "2'":
            self.domain = input("Please enter the domain to index (e.g. e.wikipedia.org): ")
            start = input("Please enter a full url within the domain to begin at (e.g. https://en.wikipedia.org/wiki/Main_Page): ")
            if self.client_wrapper.visited_col.find_one( {"url": start} ) is None and self.client_wrapper.queue_col.find_one( {"url": start} ) is None:
                self.client_wrapper.queue_col.insert_one( {"url": start} )
            self.bfs(self.get_next())
        else:
            print("Invalid input to get_start.")
            sys.exit(1)

    def get_next(self):
        # Return first existing document in the queue
        if self.client_wrapper.queue_col.count_documents({}, limit = 1):
            output = self.client_wrapper.queue_col.find_one_and_delete({}, sort={'_id': 1})["url"]
            return output
        # Otherwise end program
        else:
            print("Wasn't able to find anything in queue. Stopping.")
            self.client_wrapper.client.close()
            sys.exit(1)

    def bfs(self, url):
        self.client_wrapper.visited_col.insert_one( {"url": url} )
        try:
            html_text = requests.get(url).text
        except:
            print("Failed to open", url)
        doc = BeautifulSoup(html_text, 'html.parser')
        parsed_url = urlparse(url)
        
        print("Searching links in", url)

        # Handle each link in the document
        for link in tqdm(doc.find_all('a')):
            l = (link.get('href'))
            new_l = self.link_fixer.fixup_link(l, parsed_url)

            # Do nothing if link has already been visited
            if self.client_wrapper.visited_col.find_one( {"url": new_l} ) is not None or self.client_wrapper.queue_col.find_one( {"url": new_l} ) is not None:
                continue
            
            # Add fixed url to bfs queue
            new_parsed_url = urlparse(new_l)
            if new_l is not None and (self.domain is None or self.link_fixer.in_domain(self.domain, new_parsed_url)):
                self.client_wrapper.queue_col.insert_one( {"url": new_l} )
        
        # End program if queue is empty, otherwise returns next url and continue bfs
        next_url = self.get_next()
        self.bfs(next_url)