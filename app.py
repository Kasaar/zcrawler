import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from io import StringIO
from os.path import dirname

start = "https://localhost/test/test.html"

crawled = []

def bfs(url):
    
    html_text = requests.get(url).text
    doc = BeautifulSoup(html_text, 'html.parser')
    
    parsed_url = urlparse(url)
    
    # Handle each link in the document
    for link in doc.find_all('a'):
        l = (link.get('href'))

        if (len(l) < 2):
            continue
            
        # Handle '/' links
        elif (len(l) > 1 and l[0] == '/' and  l[0:2] != '//'):
            link_builder = StringIO()
            link_builder.write(parsed_url.scheme)
            link_builder.write("://")
            link_builder.write(parsed_url.hostname)
            link_builder.write(l)
            l = link_builder.getvalue()
            print(l)
            
        # Handle '//' links
        elif (len(l) > 1 and l[0:2] == '//'):
            link_builder = StringIO()
            link_builder.write(parsed_url.scheme)
            link_builder.write(":")
            link_builder.write(l)
            l = link_builder.getvalue()
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
            print(l)
            
        # Handle 'javascript:' links
        elif (len(l) > 11 and l[0:11] == 'javacript:'):
            continue
        
        # Handle 'mailto:' links
        elif (len > 7 and l[0:7] == 'mailto:'):
            continue
        
        # Handle remaining links
        elif (len(l) > 5 and l[0:5] != 'https' and l[0:4] != 'http'):
            link_builder = StringIO()
            link_builder.write(parsed_url.scheme)
            link_builder.write("://")
            link_builder.write(parsed_url.hostname)
            link_builder.write(l)
        
bfs(start)