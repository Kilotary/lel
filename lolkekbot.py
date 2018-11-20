import requests
import lxml.html as html
import datetime

class LelKekBot:

    def __init__(self,token):
        self.token = token
        self.apiUrl = "https://api.telegram.org/bot{}/".format(token)

    def getUpdates(self,offset=None, timeout = 30):
        method = 'getUpdates'
        params = {'timeout':timeout,'offset':offset}
        resp = requests.get(self.apiUrl + method,params)
        resultJson = resp.json()['result']
        return resultJson

    def getLastUpdate(self):
        getResult = self.getUpdates()
        if len(getResult)>0:
            lastUpdate = getResult[-1]
        else: lastUpdate = getResult[len(getResult)]    
        return lastUpdate

    def sendMess(self, chatId, text):
        params = {"chat_id":chatId, "text":text}
        method = 'sendMessage'
        response = requests.post(self.apiUrl+method,params)

    def getYoutubeFirstResult(self, url, searchparam):
        search = "/results?search_query="
        req = requests.get(url + search + searchparam )
        ydoc = html.document_fromstring(req.text())
        for a in ydoc.xpath("//a"):
            res = a.get('href')
            if res[1:6] == 'watch':
                break
        return url + res    

token = "700076471:AAG9HAUfDiPKH4QWaD995F68Pga2cE2q5KA"
bot = LelKekBot(token)
youtubeURL = "http://youtube.com"   
def main():
    newOffset = None

    while True:
        bot.getUpdates(newOffset)
        lastUpdate = bot.getLastUpdate()

        lastUpdateId = bot.lastUpdate['update_id']
        lastChatText = bot.lastUpdate['message']['text']
        lastChatId = bot.lastUpdate['message']['chat']['id']
        lastChatName = bot.lastUpdate['message']['chat']['first_name']
        lastChatTextSplit = lastChatText.split()
        searchparam = ''
    
        if lastChatTextSplit[0].lower() == '!vid':
            for p in lastChatUpdateSplit:
                searchparam += p + '+'
            searchparam = searchparam[0,-1]
            res = bot.getYoutubeFirstResult(youtubeURL, searchparam)
            bot.sendMess(lastChatId, res)
            
        newOffset = lastUpdateId +1    

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
        


