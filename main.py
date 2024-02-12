import app

if __name__ == "__main__":
    usr_input = ""
    while usr_input != "1" and usr_input != "2":
        print(usr_input)
        usr_input = input("Please enter either 1 or 2 to proceed:\n"
            + "=================================================\n"
            + "(1) Crawl the entire web. Will automatically pick up where you left off, or start from the beginning if no existing data is detected.\n"
            + "(2) Crawl a specific directory. Will request a starting point if no existing data is detected.\n"
            + "=================================================\n")

    crawler = app.Crawler()
    start = crawler.get_start(usr_input)
    crawler.bfs(start)