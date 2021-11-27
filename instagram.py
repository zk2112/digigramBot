from logging import exception
from instabot import Bot
import os
import shutil
import json
import requests
import jdatetime
from datetime import datetime
import time
import random
MAX_REQUEST=190

def clean_up(code,path=''):
   
    if code==1:
        dir = "config"
        # checking whether config folder exists or not
        if os.path.exists(dir):
            try:
            # removing it because in 2021 it makes problems with new uploads
                shutil.rmtree(dir)
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))
    if code==2:      
        remove_me = "{}.REMOVE_ME".format(path)    
        if os.path.exists(remove_me):
            src = os.path.realpath(path)
            os.rename(remove_me, src)
    if code==3:
        if os.path.exists(path):
            try:
                for f in os.listdir(path):
                    os.remove(os.path.join(path, f))
                #shutil.rmtree(path)
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))
                

def download(src):
    rand=random.randint(1,10000)
    name='images\\{}.jpg'.format(rand)
    clean_up(2,name)
    with requests.get(src,stream=True) as r:
        with open(name,'wb') as f :
            for img in r.iter_content(chunk_size=1024):
                f.write(img)
    return name
def DeletAll(bot):
    medias=bot.get_total_user_medias(bot.user_id)
    #medias1=bot.get_your_medias(as_dict=True)
   # bot.delete_medias(medias)
    if medias :
        for media in medias :
           bot.api.delete_media(media)

def percent_post(bot,p):
    if p==20 :
        clean_up(2,'date\\20.jpg')
        bot.upload_photo('date\\20.jpg',caption='تخفیف های بالای ۲۰ درصد در ادامه...')
    elif p==40 :
        clean_up(2,'date\\40.jpg')
        bot.upload_photo('date\\40.jpg',caption='تخفیف های بالای ۴۰ درصد در ادامه ...')
    elif p ==60 :
        clean_up(2,'date\\60.jpg')
        bot.upload_photo('date\\60.jpg',caption='تخفیف های بالای ۶۰ درصد در ادامه...')

def check_requests(bot):
    global MAX_REQUEST
    if bot.api.total_requests > MAX_REQUEST :
        MAX_REQUEST=MAX_REQUEST+200
        print("INFO  : total_request ={} , MAX = {}".format(bot.api.total_requests,MAX_REQUEST))
        time.sleep(2000)

def special_post(bot):
    path='date\\0.jpg'
    clean_up(2,path)
    bot.upload_photo(path)

    today=jdatetime.date.today()

    path1='date\day\{}.jpg'.format(today.day)
    clean_up(2,path1)
    bot.upload_photo(path1,caption='تخفیف های امروز'+today.strftime('%Y/%m/%d'))
    
    path2='date\month\{}.jpg'.format(today.month)
    clean_up(2,path2)
    bot.upload_photo(path2,caption='تخفیف های امروز'+today.strftime('%Y/%m/%d'))
    check_requests(bot)


clean_up(1)
bot = Bot()
while True :
    try: 
        bot.login(username = "*******", 
            password = "*******") 
        break
    except Exception as e: 
        print ('*****************login exception!**********************'+e)
        time.sleep(300)
check_requests(bot)
special_post(bot)
time.sleep(30)        

file=open('info.json','rb')
dict=json.load(file)
dict.sort(key=lambda x:int(x['percent'].replace('٪','')))
itemsList=dict.copy()
result=None
downTo=20          
try:
    for item in dict :
    
        p=int(item['percent'].replace('٪',''))
        if p>=downTo:  
            percent_post(bot,downTo)   #special post
            downTo=downTo+20
    
        photo_name=download(item['src'])
        jalali=jdatetime.date.fromgregorian(date=datetime.strptime(item['time'],'%Y-%m-%d %H:%M:%S').date())   #date To jalali
        tags=""
        for tag in item['hashtags']:
           tags=tags+'#'+tag.replace(' ','_').replace('،','#')
   
        pr='-'
        for txt in item['properties']:
            pr=pr+txt.strip()+'\n-'

        caption = ".\n{name}\n قیمت فعلی: {price}\nقیمت قبل :{old_price}\n\
                درصد تخفیف= {percent}\n تاریخ اتمام تخفیف : {time}\n\
                ویژگی ها:\n {properties}\n\
                    لینک خرید و اطلاعات بیشتر در بالای صفحه (بیو) قرار دارد.\n\
                {tags}"
        caption=caption.format(name=item['name'],price=item['price'],old_price=item['old_price'],
                            percent=item['percent'],time=jalali.strftime('%Y/%m/%d %H:%M:%S'),
                             tags=tags,properties=pr)
        result=bot.upload_photo(photo_name, 
                  caption =caption)
        if result : 
            itemsList.remove(item)
        time.sleep(30)
        check_requests(bot)

except Exception as e: print(e)
except : print ("eeeeeeeeeeeee")     #TODO
finally:    
    clean_up(3,'images')
    print("images deleted")
    print("writing...")
    file2=open('info.json','w',encoding='utf_8') 
    json.dump(itemsList,file2,ensure_ascii=False)