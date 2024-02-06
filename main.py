import app

if __name__ == "__main__":
    input = input("Specify a directory to crawl. To crawl the entire internet, type '*': ")
    
    if input == '*':
        crawler = app.Crawler()
        start = crawler.get_start()
        crawler.bfs(start)