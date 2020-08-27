import json
from crawler import Crawler


def main():
    """
    Creates a client instance. Allows user to enter commands
    to interact with the client.

    Args:
        None

    Returns:
        None
    """
    client = Client("http://example.webscraping.com")
    while True:
        values = input("Enter a command:\n").split()
        try:
            command = values[0]
        except:
            command = None 

        if command == "build":
            client.build()
        elif command == "load":
            client.load()
        elif command == "print":
            client.print_index(values[1])
        elif command == "find":
            client.find(values)
        elif command == "quit":
            print("Bye")
            return
        else:
            print("command not found. Try again")


class Client():
    """
    Client for crawler.
    """

    def __init__(self, url):
        """
        Initialises a crawler client. 

        Args:
            url: url of site to be crawled.

        Returns:
            None
        """
        self.url = url
        self.build_done = False
        self.data = None
        
    def build(self):
        """
        Performs a crawl process on a site.

        Args:
            None

        Returns:
            None
        """
        crawler = Crawler(self.url)
        crawler.crawl() 
        self.build_done = True

    def load(self):
        """
        Loads data from json file containing inverted index.

        Args:
            None
        
        Returns:
            None
        """
        if self.build_done == False:
            print("Warning, you are attempting to load without building.")
        try:
            with open("./index.json") as json_file:
                self.data = json.load(json_file)
                print("data loaded successfully.")
                return
        except:
            print("error reading file")
            return

    def print_index(self, word):
        """
        Prints the inverted index of a query in decending 
        order of relevance.

        Args:
            word: query word.
        
        Returns:
            None
        """
        if self.data is None:
            print("You must load before retrieving index.")
            return
        try:
            index = self.data.get(word)
            if index is None:
                print(f"{word} not found in index")
            else:
                for key, value in sorted(
                        index.items(), reverse=True, 
                        key=lambda item: item[1]):
                    print(f"{key} - {value} matches")
        except:
            print(f"{word} not found in index")

    def find(self, words):
        """
        Find pages containing query words from the inverted 
        index in decending order of relevance.

        Args:
            words: query words.
        
        Returns:
            None
        """
        if self.data is None:
            print("You must load before retrieving index.")
            return    

        queries = []
        all_urls = []
        results = []

        for word in range(1,len(words)):
            queries.append(words[word])
       
        for query in queries:
            urls = self.data.get(query)
            if urls is None:
                print("No results found")
                return 
            else:
                for url in urls:
                    all_urls.append(url)

        for url in all_urls:
            valid = 0
            # check that url is valid for all queries
            for query in queries:
                urls = self.data.get(query)
                if urls is None or url not in urls:
                    valid += 1
            if valid == 0:   
                if url not in results:
                    results.append(url)
           
        final = {}
        # get occurances of all queries for each link
        for result in results:
            matches = 0
            for query in queries:
                urls = self.data.get(query)
                counter = urls.get(result)
                matches += counter 
            final[result] = matches

        # print in order of relevance
        for key, value in sorted(final.items(), reverse=True, key=lambda item: item[1]):
            print(f"{key} - {value} matches")


if __name__ == "__main__":   
    main()