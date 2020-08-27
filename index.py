import json

class InvertedIndex():
    """
    Class representing an inverted word index. 
    """

    def __init__(self):
        """
        Initialses class with empty word index.
        """
        self.word_index = {}
    
    def create_index(self, url, words):
        """
        Creates an inverted index from the pages than contain 
        requested words.

        Args:
            url: url of the crawled page.
            words: words that exist in the page. 

        Returns:
            None
        """

        for word in words:
            if word not in self.word_index:
                value = {
                    url: 1
                }
                self.word_index[word] = value
            else:
                if url in self.word_index[word]:
                    self.word_index[word][url] += 1
                else:
                    self.word_index[word][url] = 1

        # w mode - start from empty file each time        
        with open("index.json", "w") as output:  
            json.dump(obj=self.word_index, fp=output, indent=4)

