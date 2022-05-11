#-*- coding: utf-8 -*-
# any thing you want
from operator import le
import re
import scrapy
import sys
import random


 


class AmazonSpider(scrapy.Spider):
    name = 'amazon1000'
 
    abc=open('/home/moglix/Desktop/amazon1000.txt').read().splitlines()
    data_analysy={}
    for intercept_url in abc:
            ur_l=intercept_url
            base_url=ur_l.split('||')[0]
            msn_url=ur_l.split('||')[1]
            data_analysy[base_url]=msn_url
            #print(base_url,msn_url)

    start_urls=data_analysy.keys()

    #start_urls=abc
    
    def parse(self, response):
        data={}
        
        r1=(response.xpath("//div[contains(@class,'a-section')]/div[contains(@class,'sg-row')]")).getall()
        #r1=(response.xpath("//a[contains(@class,'a-link-normal s-no-outline')]/@href")).getall()
        print(len(r1))
        if(len(r1)==1):
            r1=(response.xpath("//div[contains(@class,'a-section a-spacing-base')]")).getall()

        p_id=''
        substring="/dp"
        sub_sponsered="Sponsored"
        amzaon_url="https://www.amazon.in/product-reviews/"
        filter_url="?filterByStar=positive&reviewerType=all_reviews&pageNumber=1"
        response_urls=response.url.replace('%20',' ')
        msn_urls=AmazonSpider.data_analysy[response_urls]
        intem_start=0
        print("lenght of data scrapped",len(r1))
        for ret in r1:
              if substring in ret:
               #print(intem_start)
               if intem_start <len(r1): 
                 pid_str=re.split('dp/',ret)[1]
                 product_id=re.split('/ref',pid_str)[0]
                 if product_id in p_id:
                   #print("exist "+product_id)
                   continue
                 else:
                     #print("hellao "+ret)
                     #check the prdouctID is sponsered or not
                     if sub_sponsered in ret:
                         print( " id sponsered sponserd ")
                         continue
                     else:
                         intem_start=intem_start+1
                         print("intem_start",intem_start)
                         if(len(p_id)==0):
                             #capture the url first_four_word_count
                              u_R_L=response.url.split('k=')[1].replace('%20',' ')
                              #print("U_R_L",u_R_L)
                              #capture word count 
                              word_count=len(u_R_L.split())
                              if(float(word_count)>=4):
                                  words_count_array=u_R_L.split(' ')
                                  searc_items_words=''
                                  index=0
                                  for w in words_count_array:
                                      if(index==0):
                                          searc_items_words=w
                                      if(index>0 and index <=1):
                                          if("boAt" in ret):
                                              print("Boat")
                                              searc_items_words=searc_items_words+' '+w
                                          else:
                                              searc_items_words=searc_items_words+' '+w
                                              if("Sony" in ret or "Zebronics" in ret):
                                                 index=index+1
                                      index=index+1
                                  if("In" in searc_items_words):
                                      searc_items_words=searc_items_words.replace('In','')
                                  if("in" in searc_items_words):
                                      searc_items_words=searc_items_words.replace('in','')
                                  
                                  print("word should present in ",searc_items_words)
                                  #print(" ret ",ret)
                                  if(searc_items_words in ret):   
                                     p_id=amzaon_url+product_id.strip()+filter_url+"||"+msn_urls
                                     print("Non Sponsered productId"+p_id)
                         
               else:
                   #print("break")
                   break
        #add to failed url
        #print(len(p_id))
        if len(p_id)==0 :
             filet=open('failed_netmart.txt','a')
             filet.write((str(response.url).replace('%20',' '))+"||"+msn_urls+"\n")
        
        data={
            'Product_Id':p_id,
            'url':response.url
            
        }
        
        yield data

