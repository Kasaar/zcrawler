
zcrawler
==========

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](https://choosealicense.com/licenses/mit/)

A web crawler built in Python for use in indexing projects and search engine population.
Uses MongoDB and the pymongo driver to intelligently store and query data from a non-relational
database. Capable of either indexing a specifc domain for use in application-specific search,
or indexing the entirety of the internet. Advances using breadth-first search through embedded
URLs in previously accessed webpages.

## Installation and Dependencies ##

zcrawler uses `pymongo` for database operations, `requests` for HTML requests,
`BeautifulSoup` for HTML parsing, and `urllib` for URL parsing.

    python -m pip install "pymongo[srv]"
    pip install requests
    pip install beautifulsoup4
    pip install tqdm

### Installation ###

The recommended way to obtain the source code is to clone the entire
[repository](https://github.com/Kasaar/zcrawler) from
[GitHub](https://github.com)

    git clone https://github.com/Kasaar/zcrawler.git

### Usage ###

Run the following command to begin the application:

    python3 main.py

You will be prompted to enter an input indicating the scope of your
search. Enter `1` to begin a search of the entire web, or enter `2`
to limit your search to a specific domain (e.g. only find pages in
the wikipedia domain). Option `1` is designed for use in gathering
data for full-web search engines, and option `2` is designed for use
in gathering data for site-specific search engines.

Next, you will be prompted to enter a valid MongoDB URI. Any valid
cluster should work: zcrawler will create the relevant collections.
See the following section to learn more about MongoDB URIs.

If you selected option `2`, you will be further prompted to enter
a domain to search, and a URL to begin at. Enter the domain as
a hostname of the form `en.wikipedia.com` and the URL as a
specific page of the form `https://en.wikipedia.org/wiki/Main_Page`.

To stop the crawler prematurely, press `ctrl` + `c`.

### MongoDB ###

MongoDB offers a free option for hosting a cluster using Atlas.
You can sign up at https://www.mongodb.com/cloud/atlas/register.

To obtain the URI for a cluster using Atlas:
1. Log in to MongoDB
2. Navigate to Security -> Database Access
3. Find a user and password with sufficient permissions and input them into the form below:
4. mongodb+srv://<db_username>:<db_password>@cluster0.9vyo3he.mongodb.net/?retryWrites=true&w=majority&appName=<cluster_name>
Where `<db_username>`, `<db_password>`, and `<cluster_name>` are dependent on your implementation.

https://pymongo.readthedocs.io/en/stable/examples/tls.html