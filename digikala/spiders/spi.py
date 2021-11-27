from re import T
import scrapy
from scrapy.selector import Selector
from ..items import DigikalaItem
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

class SpiSpider(scrapy.Spider):
    name='spi'
    start_urls=[
        'https://www.digikala.com',
    ]
    info=[]
    def parse(self,response):
         
        driver=webdriver.Firefox()
        driver.get('https://www.digikala.com/incredible-offers/')
        # waiting to load
        try:
           element = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME,'div'))
            )
        except:
           print('*********************************************************')     #TODO   handle exception
       # time.sleep(3)
        #scroll to load all of items
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True  :
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            '''try:
               element = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME,'div'))
                )
            except:
               print('###########################')     #TODO   handle exception
            '''
            time.sleep(5)

            myscroll_height= driver.execute_script("return document.body.scrollHeight")

            if myscroll_height==last_height :
                break

            last_height=myscroll_height
        
        #exteract fileds
        sel=Selector(text=driver.page_source)
        
        
        for item in sel.css('div.c-product-list__item'):
            data=DigikalaItem()
            if item.css('div.js-ab-not-app-incredible-product ::text').get() :
               data['name']= item.css('div.js-ab-not-app-incredible-product ::text').get().strip()
            else : continue

            if item.css('del.js-product-card-price ::text').get() :
                data['old_price']=item.css('del.js-product-card-price ::text').get()
            else : continue

            if item.css('div.c-price__value-wrapper  ::text').get():
                data['price']=item.css('div.c-price__value-wrapper  ::text').get().strip()
            else: continue

            if item.css('div.c-price__discount-oval span ::text').get():
                data['percent']=item.css('div.c-price__discount-oval span ::text').get()
            else:continue

            if item.css('div.c-product-box__timer ::attr(data-countdown)').get() :
                data['time'] = item.css('div.c-product-box__timer ::attr(data-countdown)').get()
            else:continue

            if item.css('div.c-product-box__img img::attr(src)').get():
                data['src']=item.css('div.c-product-box__img img::attr(src)').get()
            else:continue
            
            
            if item.css('a ::attr(href)').get() :

                link=response.urljoin(item.css('a ::attr(href)').get())
                data['link']=link
                yield scrapy.Request(url=link,callback=self.parse2,cb_kwargs=dict(arg=data.copy()),errback=self.err,dont_filter=True)
            else :  continue
            
           # yield self.data
        #data['accession']=names
        #data['image_urls']=product
        #yield data 
    def parse2(self,response,arg):
        
        #arg['title']=response.css('h1.c-product__title ::text').get()
        hashtag=response.css('a[property="item"] span ::text').getall()
        
        arg['hashtags']=hashtag
        properties=response.css('div.c-product__params ul li span ::text').getall()
        temp=[]
        
        for i in range(0,len(properties),2):
            temp.append(properties[i].strip()+properties[i+1].strip())
     
        arg['properties']=temp
        self.info.append(dict(arg))
        yield arg
    def err(self,request):
        self.logger.info('#################################################errorback')
    
    def __del__(self):
        file2=open('info.json','w',encoding="utf-8") 
        json.dump(self.info,file2,ensure_ascii=False)

