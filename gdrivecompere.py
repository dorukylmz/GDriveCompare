from Google import Create_Service
import os
import datetime
import sys
import requests
import time

# def getDays():
#     today = datetime.datetime.now()
#     today = str(datetime.datetime.date(today))
#     today = today[:4]+"_"+today[5:7]+"_"+today[8:10]

#     yesterday = datetime.datetime.now()-datetime.timedelta(days=1)
#     yesterday = str(datetime.datetime.date(yesterday))
#     yesterday = yesterday[:4]+"_"+yesterday[5:7]+"_"+yesterday[8:10]

#     tomorrow = datetime.datetime.now()+datetime.timedelta(days=1)
#     tomorrow = str(datetime.datetime.date(tomorrow))
#     tomorrow = tomorrow[:4]+"_"+tomorrow[5:7]+"_"+tomorrow[8:10]
#     days={'today': today, 'tomorrow':tomorrow, 'yesterday':yesterday}
#     return days

def querytofolderdrive(folderID='FolderID'):
    CLIENT_SECRET_FILE = 'googlesec.json'
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    # days=getDays()
    query = f"parents='{folderID}' "
    result = service.files().list(q=query).execute()
    files = result.get('files')
    nextPageToken = result.get('nextPageToken')

    while nextPageToken:
        result = service.files().list(q=query).execute()
        files.extend(result.get('files'))
        nextPageToken = result.get('nextPageToken')

    return files



def getListofFiles(folderlocation):
    listoffiles=[]
    paths=[]
    for path, subdirs, files in os.walk(folderlocation):
        for name in files:
         listoffiles.append(name)
         paths.append(path)         


    return listoffiles,paths    


def getListOfCloud(folderID=None, files=[]):
    if folderID == None:
        file = querytofolderdrive()
    else:
        file = querytofolderdrive(folderID)
    for item in file:
        files.append(item['name'])
        print(item['mimeType'])
        if item['mimeType'] == 'application/vnd.google-apps.folder' :
            print("gidilen klasör " + item['name'])
            getListOfCloud(item['id'], files=files)
        else:
            print("atlanıldı")    

    return files


def filterList(filelist,paths=[]):
    # 3 günlük olarak bakılması daha uygun
    newlist = []
    newpaths= []
    today = datetime.datetime.now()
    today = str(datetime.datetime.date(today))
    today = today[:4]+"_"+today[5:7]+"_"+today[8:10]

    yesterday = datetime.datetime.now()-datetime.timedelta(days=1)
    yesterday = str(datetime.datetime.date(yesterday))
    yesterday = yesterday[:4]+"_"+yesterday[5:7]+"_"+yesterday[8:10]

    tomorrow = datetime.datetime.now()+datetime.timedelta(days=1)
    tomorrow = str(datetime.datetime.date(tomorrow))
    tomorrow = tomorrow[:4]+"_"+tomorrow[5:7]+"_"+tomorrow[8:10]

    # String olarak karşılaştırılıyor
    i=0
    if paths==[]:
        for item in filelist:
            if item.find(today) != -1 or item.find(yesterday) != -1 or item.find(tomorrow) != -1:
                newlist.append(item)
        return newlist
    else:
        for item in filelist:
            if item.find(today) != -1 or item.find(yesterday) != -1 or item.find(tomorrow) != -1:
                newlist.append(item) 
                newpaths.append(paths[i])
        i+=1
        return newlist,newpaths


def compare(drivelist=[],filelist=[],paths=[]):
    notsyclist=[]
    notsycpathlist=[]
    i=0
    for item in filelist:
      match=False
      for x in drivelist:
        if x==item:
           match=True 

      if match==False:
        notsyclist.append(item)
        notsycpathlist.append(paths[i])
      i+=1
    
    return notsyclist,notsycpathlist

def sendMessage(object,paths):
    if object==[]:
       messagevar="Bütün dosyalar senknonize"
       requests.get(f"telegramkey={messagevar}")
    
    else :
        messagevar=f"senkronize olamayan dosya sayısı = {len(object)}\nAşağıdaki dosyalar senksonize olamadı;"
        requests.get(f"telegramkey={messagevar}")
        i=0 
        #Apiye sığmadığı için bölü göndermem gerek
        for file in object:
            requests.get(f"telegramkey={messagevar}")



def main(folderloc):
#dışarıdan çağırabilmek için main def şeklinde
   
    drivefilelist = []
    drivefilelist = getListOfCloud()
    drivefilelist = filterList(drivefilelist)
    print(f"drivefiles:\n{drivefilelist}")
    print("\n\n\n\n")
    folderlist=[]
    folderlist,paths= getListofFiles(folderlocation=folderloc)
    folderlist,paths= filterList(filelist=folderlist,paths=paths)
    print(f"folders:\n{folderlist}")
    print("\n\n\n\n")
    print(f"paths:\n{paths}")
    print("\n\n\n\n")
    Notsyncfiles,notsycpaths=compare(drivelist=drivefilelist,filelist=folderlist,paths=paths)
    print(f"NotSyncfiles:\n{Notsyncfiles}")
    print("\n\n\n\n")
    print(f"notSyncPaths:\n{notsycpaths}")
    print("mesaj gönderiliyor")
    sendMessage(object=Notsyncfiles,paths=notsycpaths)

folderloc=sys.argv[1]
messagevar="Senkronizasyon Doğrulanıyor, Günaydın."
#requests.get(f"telegramkey={messagevar}")
main(folderloc=folderloc)