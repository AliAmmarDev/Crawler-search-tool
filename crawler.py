import time
import requests
from bs4 import BeautifulSoup
from index import InvertedIndex

class Crawler():
    """
    Class for crawling pages on a website. 
    """
    def __init__(self, url):
        """
        Initialises class with base url of the website. 

        Args:
            url: url of website to be crawled. 

        Returns:
            None
        """
        self.url = url
        self.urls = ["/places/default/index"]
        self.crawled_urls = []
        
    def crawl(self):
        """
        Performs a crawl process on each pending page. 

        Args:
            None
        
        Returns:
            None
        """

        index = InvertedIndex()

        for url in self.urls:    
            if url not in self.crawled_urls:

                # build page 
                response = requests.get(f"{self.url}{url}")
                page_object = BeautifulSoup(response.content, "html.parser")

                # begin crawling
                print(f"Crawling: {url}")
                self.links(page_object)
                page = f"{self.url}{url}"
                words = self.words(page_object)
                index.create_index(page, words)

                # mark page as visited
                self.crawled_urls.append(url)
                self.urls.remove(url)

                time.sleep(5)

    def links(self, page):
        """
        Extracts the url links found in a page. 

        Args:
            page: parsed HTML page. 
        
        Returns:
            None
        """

        for link in page.find_all('a'):
            register_url = "places/default/user/register?_next=/places/default/"
            login_url = "places/default/user/login?_next=/places/default/"

            url = link.get('href')
            skip = False

            # ensure login/sign up page is crawled only once
            if register_url in url or login_url in url:
                if url != f"{register_url}index" and url != f"{login_url}index":
                    skip = True

            # no need to crawl edit pages
            if "edit" in url:
                skip = True

            if skip == False:
                self.urls.append(url)

    def words(self, page):
        """
        Extracts the data found in given tags. 

        Args:
            page: parsed HTML page. 

        Returns:
            words: list of found words.
        """
        tags = ["td","h1","h2","h3","li"]
        words = []
        for tag in tags:
            for element in page.find_all(tag):
                for word in element.text.split():
                    word = word.replace(":","")
                    words.append(word)
        
        return words
        
