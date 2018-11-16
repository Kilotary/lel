import requests
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
        return response

token = "700076471:AAG9HAUfDiPKH4QWaD995F68Pga2cE2q5KA"
bot = LelKekBot(token)
greet = ('здраствуй','привет','ку','хдорово')
now = datetime.datetime.now()

def main():
    newOffset = None
    today = now.day
    hour = now.hour

    while True:
        bot.getUpdates(newOffset)

        lastUpdate = bot.getLastUpdate()

        lastUpdateId = lastUpdate['update_id']
        lastChatText = lastUpdate['message']['text']
        lastChatId = lastUpdate['message']['chat']['id']
        lastChatName = lastUpdate['message']['chat']['first_name']
        bot.sendMess(lastChatId,'Huli Nado,{}'.format(lastChatName))


        
        if lastChatText.lower() in greet and today == now.day and 6<=hour<=12:
            bot.sendMess(lastChatId,'Доброе утро,{}'.format(lastChatName))
            today += 1
        if lastChatText.lower() in greet and today ==now.day and 12<=hour<=17:
            bot.sendMess(lastChatId,'Доброе день,{}'.format(lastChatName))
            today += 1
        if lastChatText.lower() in greet and today ==now.day and 17<=hour<=23:
            bot.sendMess(lastChatId,'Доброе вечер,{}'.format(lastChatName))
            today += 1    

        newOffset = lastUpdateId +1    

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
