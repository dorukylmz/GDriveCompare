from gdrivecompere import main
from datetime import datetime,timedelta
import requests
import json
import time
import sys
import logging


bot_key="TelegramBotKey"
lastmessage=None
compare="/Compare"
nasılsın="/nasılsın"
Nasılsın="/Nasılsın"
backuplocation=sys.argv[1]
logging.basicConfig(filename='botapi.log', encoding='utf-8', level=logging.DEBUG)

def getUpdates():
    #bağlantı koparsa tekrar denemesi için 
    try:
         response=requests.get(f"{bot_key}getupdates")
         return response
    except:
            i=False
            while i==False:
                    try:
                      response=requests.get(f"{bot_key}getupdates")
                      i=True
                      return response       
                    except:
                        pass

try:
    while True:
            response=None
            while True:
                response=getUpdates()
                #cevap başarılı olup olmadığını kontrol etmesi için vew başarısızsa bir daha koştursun
                if response.status_code==200:
                    try:
                        data=json.loads(response.text)
                        newmessageid=(data['result'][(len(data['result'])-1)]['message']['message_id'])
                        break
                    except:
                       newmessageid=lastmessage
             
            
            if lastmessage!=newmessageid:
              
                if (data['result'][(len(data['result'])-1)]['message']['text'])==compare:
                    try:
                        requests.get(f"{bot_key}sendMessage?chat_id=-&text=Karşılaşrıtılıyor")
                    except:
                        i=False
                        while i==False:
                            try:
                                requests.get(f"{bot_key}sendMessage?chat_id=-&text=Karşılaşrıtılıyor")
                                i=True    
                            except:
                                    pass

                    main(folderloc=backuplocation)
                    lastmessage=newmessageid
                    time.sleep(10)
                
                elif (data['result'][(len(data['result'])-1)]['message']['text'])==nasılsın or (data['result'][(len(data['result'])-1)]['message']['text'])==Nasılsın  :
                    try:
                        requests.get(f"{bot_key}sendMessage?chat_id=-&text=Sorunsuz Çalışmakta")
                    except:
                        i=False
                        while i==False:
                            try:
                                requests.get(f"{bot_key}sendMessage?chat_id=-&text=Sorunsuz Çalışmakta")
                                i=True    
                            except:
                                    pass

                    lastmessage=newmessageid
                    time.sleep(10)

                else:
                    try:
                        requests.get(f"{bot_key}sendMessage?chat_id=-&text=Ne dediğini anlayamıyorum\n-Senkronize dosyaları kontrol etmek için : \\Compare\n-Durumu kontrol etmek için: \\nasılsın \n yazabilirsiniz.")
                    except:
                        i=False
                        while i==False:
                            try:
                                requests.get(f"{bot_key}sendMessage?chat_id=-&text=Ne dediğini anlayamıyorum\n-Senkronize dosyaları kontrol etmek için : \\Compare\n-Durumu kontrol etmek için: \\nasılsın \n yazabilirsiniz.")
                                i=True    
                            except:
                                    pass

                    lastmessage=newmessageid
                    time.sleep(10)



            else :
                time.sleep(10)
           
except Exception as e:
            try:
                logging.critical(e)
                main()
            except:
                logging.critical(f"{e}")
                main()