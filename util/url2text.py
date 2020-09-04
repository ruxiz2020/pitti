import requests
from bs4 import BeautifulSoup
#import base64
#from langdetect import detect


class Url2Text:

    def __init__(self, url):
        """
        Extract text data from url
        """
        self._url = url

        response = requests.get(self._url)
        data = response.content.decode('utf-8', errors="replace")

        self._soup = BeautifulSoup(data, "lxml")

    def _get_title(self):

        try:
            title_ = self._soup.find('title')
            title = title_.getText()
        except:
            try:
                title_ = self._soup.find('h1')
                title = title_.getText()
            except:
                title = "NA"
        return title

    def extract_text_from_html(self):

        title = self._get_title()
        #try:
        #    title = title_.getText()
        #except:
        #    title = "title"

        page = self._soup.findAll('p') # works for wikipedia
        #page = self._soup.findAll(["div", {"class" : re.compile('*paragraph*')},]) # works for cnn news

        sentences = []
        for pp in page: # loop over all <p> sentence</p>

            text = pp.getText().strip()

            sentences.append(text)
            # print(text)

        paragraph = ' '.join(sentences)
        return title, paragraph


if __name__ == "__main__":

    #url = "https://pets.webmd.com/cats/cat-fip-feline-infectious-peritonitis#1"
    #url = "https://mp.weixin.qq.com/s/mvmbJsORjsLjGfpz5yScWg"
    #url = "https://en.wikipedia.org/wiki/Kubernetes"
    url = "https://www.cdc.gov/healthypets/diseases/cat-scratch.html"
    print(url)

    extractText = Url2Text(url)
    title, sentences = extractText.extract_text_from_html()

    print(title)
    print(sentences)
    print(len(sentences))

    #file = open("../read_it/test.txt", "w")
    #file.write(text)
    #file.close() #This close() is important
