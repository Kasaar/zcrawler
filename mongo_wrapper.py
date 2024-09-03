from pymongo import MongoClient, errors
from pymongo.server_api import ServerApi
import sys

class MongoWrapper():
    def __init__(self):
        # Get mongo connection info from user
        uri = input("Input your MongoDB uri: ")

        # Try to connect to mongo
        try:
            self.client = MongoClient(uri, server_api=ServerApi('1'))
        # Return a friendly error if a URI error is thrown
        except errors.ConfigurationError:
            print("An Invalid URI host error was received. Is your host name correct in your connection string?")
            sys.exit(1)

        self.db = self.client["zcrawler"]
        self.queue_col = self.db["queue"]
        self.visited_col = self.db["visited"]
        self.repository_col = self.db["repository"]

# Run this file directly to test mongo connection
if __name__ == "__main__":
    client = MongoWrapper()
    print("Successfully connected.")
    client.client.close()
    sys.exit(1)
    