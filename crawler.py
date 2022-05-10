from bs4 import BeautifulSoup
import requests
from comic import comic

class crawler:
    
    my_headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36',
        'Content-Type' : 'text/html'
    }

    def crawlNew(self, inputUrl, my_headers):
        resultList = []
        try:
            r = requests.get(inputUrl, headers = my_headers)
            soup = BeautifulSoup(r.text, 'html.parser')

            startIdx = 0
            endIdx = len(soup.find_all('a', class_='active'))
            comics = soup.find_all('a', class_='active')
            print(comics)
            print(len(comics))

            if len(comics) == 0:
                return []
            else:
                for i in range(startIdx, endIdx-1):
                    newComic = comic()
                    newComic.url = comics[i].href
                    newComic.episode = comics.text
                    print(newComic)
                    resultList.append(newComic)

        except BaseException as err:
            print(err)
        return resultList