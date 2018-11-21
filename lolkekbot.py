import requests
from apiclient.discovery import build
from apiclient.errors import HttpError


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
        else:
            lastUpdate = 0    
        return lastUpdate

    def sendMess(self, chatId, text):
        params = {"chat_id":chatId, "text":text}
        method = 'sendMessage'
        response = requests.post(self.apiUrl+method,params)

    def getVideo(self, query, where):
        searchResponse = where.search().list(
                q = query,
                part='snippet',
                maxResults=5
                ).execute()

        for searchRes in searchResponse.get('items',[]):
            if searchRes['id']['kind']=='youtube#video':
                return searchRes['id']['videoId']
        
        return 'cocиписос'       

token = "700076471:AAG9HAUfDiPKH4QWaD995F68Pga2cE2q5KA"
bot = LelKekBot(token)

DEVELOPER_KEY = 'AIzaSyD3q2zJLDca75xklszgqsMsZIONdR9nUwA'
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def main():
    newOffset = None
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)
    
    while True:
        bot.getUpdates(newOffset)
        lastUpdate = bot.getLastUpdate()
        
        if lastUpdate ==0:continue
        
        lastUpdateId = lastUpdate['update_id']
        lastChatText = lastUpdate['message']['text']
        lastChatId = lastUpdate['message']['chat']['id']
        #lastChatName = lastUpdate['message']['chat']['first_name']
        lastChatTextSplit = lastChatText.split(maxsplit=1)
 
        if lastChatTextSplit[0].lower() == '!vid' and  len(lastChatTextSplit)>1:
            h = bot.getVideo(lastChatTextSplit[1], youtube)        
            bot.sendMess(lastChatId, "http://youtube.com/watch?v="+h)
  
        newOffset = lastUpdateId +1    

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
        


