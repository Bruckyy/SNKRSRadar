import requests
from time import sleep
from bs4 import BeautifulSoup
import os
import tweepy

print("up")

auth = tweepy.OAuthHandler(os.environ['CONSUMER_KEY'], os.environ['CONSUMER_SECRET'])
auth.set_access_token(os.environ['ACCESS_KEY'], os.environ['ACCESS_SECRET'])
api = tweepy.API(auth)

url = 'https://www.nike.com/fr/launch?s=upcoming'

def upload_image(text,filename):
    media = api.media_upload(filename)
    api.update_status(text,media_ids=[media.media_id_string])



while(True):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    section=soup.find('section', {"class" : "upcoming-section"})
    figures = section.findAll('figure', {"class" : "pb2-sm"})

    allImages= soup.findAll('img', {'class' : 'image-component'})
    images_list = []
    for image in allImages:
        if "https://secure-images.nike.com" in image['src']:
            images_list.append(image['src'])


    i=0
    for fig in figures:
        date = fig.find('p', {'class':'headline-1'}).text + " " + fig.find('p', {'class':'headline-4'}).text
        img = images_list[i].replace("&align=0,1","")
        name = fig.find('h3', {'class':'headline-5'}).text + " " + fig.find('h6', {'class':'headline-3'}).text
        with open("posted.txt",'r') as posted:
            if (name+date) not in posted.read():
                print(date+ ": " + name)
                print(img)
                print('\n')
                img_data = requests.get(img).content
                with open(name+".jpg", 'wb') as handler:
                    handler.write(img_data)
                with open("posted.txt",'a') as f:
                    f.write(name+date+"\n")
                try:
                 upload_image(name+"\n"+date,name+".jpg")
                 print(f"{name} : {date} | TWEETED SUCCESFULLY")
                except Exception as e:
                    print("Cannot tweet")
                    print(e)
        i+=1
    sleep(60)