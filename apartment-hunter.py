# -*- coding: utf-8 -*-
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import os
import datetime
import time
import re
import smtplib
import random

def requests_retry_session(
    retries=50,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

bazarcookies = {
    'euconsent': '',
    'uuid': '',
    '__gfp_64b': '',
    'translator': '',
    '_gat': '',
    'pl': '',
    'jwt': '',
    'bc': '',
    '__gads': '',
    'cto_lwid': '',
    'cookiechoose':'',
    '_ga': '',
    '_gid': '',
           }

mainurl = 'https://www.olx.bg/nedvizhimi-imoti/prodazhbi/sofiya/?search%5Bfilter_float_price%3Ato%5D=95000&search%5Bdescription%5D=1'
mainurlbazar = 'https://bazar.bg/obiavi/apartamenti/dvustaini/sofia?sort=date'
while True:
    server = smtplib.SMTP('IP', PORT)
    server.login("USERNAME", "PASSWORD")
    #OLX.bg
    mainurl2 = requests_retry_session().get(mainurl)
    olxsoup = BeautifulSoup(mainurl2.text.encode('utf-8'), 'html.parser')
    #print olxsoup


    for td in olxsoup.find_all('tr', {'class': 'wrap'},limit = 100):
        #print(td).encode('windows-1251')

        for i1 in td.find_all('a',limit = 2):
            Zaglavie = (i1).text.replace('\n','')
            #print i1            
            Zaglavie = re.sub((u'€'), "", Zaglavie)
            Zaglavie = re.sub((u'–'), "-", Zaglavie)
            Zaglavie = re.sub((u'“'), "", Zaglavie)
            Zaglavie = re.sub((u'”'), "", Zaglavie)
            Zaglavie = re.sub((u'„'), "", Zaglavie)
            Zaglavie = re.sub((u'\xb2'), '2', Zaglavie)
        print 'OLX: '+Zaglavie

        for i1 in td.find_all('small', {'class': 'breadcrumb x-normal'},limit = 2):
            Kvartal = (i1).text.replace('\n','').encode('utf-8')

        for i1 in td.find_all('div', {'class': 'space inlblk rel'},limit = 1):
            Cena = (i1).text
            Cena = re.sub((u'По договаряне'), "", Cena)
            Cena = re.sub((u' €'), "", Cena)
            Cena = re.sub((u' лв.'), "", Cena)
            Cena = re.sub(('\n'), "", Cena)
            #Cena = re.sub((r'\.[0-9][0-9]'), "", Cena)
            print Cena

        for i1 in td.find_all('a', limit = 1):
            i2 = i1.get('href')
            URL = (i2)[0:-11].encode('utf-8')
        print 'breakpoint1'
        f = open( 'PATHTOTEMPTXTFILE', 'r' )
        if (2000 <= int(Cena) <= 90000) and (any(re.findall(r'Младост', Kvartal, re.IGNORECASE)) or any(re.findall(r'Младост', Zaglavie, re.IGNORECASE))) and not (URL in f.read()):
            f.close()
            print 'breakpoint2'
            sizestat = os.stat('PATHTOTEMPTXTFILE').st_size
            print ('sizestat: '+str(sizestat))
            
            if sizestat >= 5242880:
                f = open('PATHTOTEMPTXTFILE', 'w')
            else: f = open( 'PATHTOTEMPTXTFILE', 'a' )
            print (Zaglavie)
            f.seek(0,2)
            f.write(Zaglavie.encode('utf-8')+'\n') 
            print ("Квартал: "+Kvartal).decode('utf-8')
            f.seek(0,2)
            f.write(Kvartal+'\n')
            print ("Цена: "+str(Cena)).decode('utf-8')
            f.seek(0,2)
            f.write(str(Cena)+'\n')
            print ("URL: "+URL+'\n').decode('utf-8')
            f.seek(0,2)
            f.write(URL+'\n\n')
            f.close()
            
            #Send the mail
            headers = ("Message-ID: <"+str(random.randint(1000000000000000000000000000,9999999999999999999999999999))+"@mailer.DOMAIN.com>\nFrom: NAME1 <user1@domain2.com>\nTo: NAME2 <user2@domain2.com>\nCC: NAME3 <user3@domain3.com>\nSubject: "+Zaglavie.encode('utf-8')+'\nMIME-Version: 1.0\nContent-Type: text/html; charset=utf-8\nContent-Transfer-Encoding: 8bit\n')
            msg = ('\n\n<!DOCTYPE html><head><meta charset="UTF-8"></head><body><p style="margin-top:0in;margin-right:0in;margin-bottom:8.0pt;margin-left:0in;line-height:107%;font-size:15px;font-family:&quot;Calibri&quot;,sans-serif;">Заглавие - '+Zaglavie.encode('utf-8')+'<br>'+"Квартал - "+Kvartal+'<br>'+"Цена - "+str(Cena)+'<br>'+"URL - "+'<a href="'+URL+'">'+URL+'</a>'+'<br></p>'+'</body></html>\n\n')
        
            server.sendmail("MAILFROMADDRESS", "MAILTOADDRESS", headers+msg)

    #OLX.bg
    #Bazar.bg

    mainurlbazar2 = requests_retry_session().get(mainurlbazar, cookies=bazarcookies)
    bazarsoup = BeautifulSoup(mainurlbazar2.text.encode('utf-8'), 'html.parser')
    #print olxsoup


    for td in bazarsoup.find_all('div', {'class': 'row-fluid clearfix list-result '},limit = 100):
        #print(td).encode('windows-1251')

        for j1 in td.find_all('div', {'class': 'title'},limit = 1):
            Zaglavie2 = (j1).text.replace('\n','').encode('utf-8')
            imotiapartamenti = (u'Имоти › Aпартаменти').encode('utf-8')
            Zaglavie2 = re.sub(imotiapartamenti, "", Zaglavie2)
            Zaglavie2 = re.sub((u'                                                '), "", Zaglavie2)
            Zaglavie2 = re.sub((u'                                            '), "", Zaglavie2)
            Zaglavie2 = re.sub((u'–'), "-", Zaglavie2.decode('utf-8'))
            Zaglavie2 = re.sub((u'€'), "", Zaglavie2)
            Zaglavie2 = re.sub((u'“'), "", Zaglavie2)
            Zaglavie2 = re.sub((u'”'), "", Zaglavie2)
            Zaglavie2 = re.sub((u'„'), "", Zaglavie2)
            Zaglavie2 = re.sub((u'…'), "...", Zaglavie2)
            #Zaglavie2 = ''.join([char if ((65 <= ord(char) <= 90) or (192 <= ord(char) <= 255)) else '' for char in Zaglavie2])
            print 'Bazar: '+Zaglavie2
            Zaglavie2 = Zaglavie2.encode('utf-8')
            

        for j1 in td.find_all('div', {'class': 'location'},limit = 1):
            Kvartal2 = (j1).text.replace('\n','').replace('                    ','').encode('utf-8')
            #print Kvartal2.decode('utf-8')

        for j1 in td.find_all('div', {'class': 'price'},limit = 1):
            Cena2 = (j1).text
            #print Cena2
            if len(Cena2)==1:
                print 'No price'
                Cena2 = str(int(0)).encode('utf-8')
            Cena2 = re.sub((u'По договаряне'), "", Cena2)
            Cena2 = re.sub((u' €'), "", Cena2)
            Cena2 = re.sub((u' лв'), "", Cena2)
            Cena2 = re.sub(('\n'), "", Cena2)
            Cena2 = re.sub((' '), "", Cena2)
            #Cena2 = re.sub((r'\.[0-9][0-9]'), "", Cena2)
            
            print Cena2.decode('utf-8')

        for j1 in td.find_all('a', {'class': 'title'}, limit = 1):
            j2 = j1.get('href')
            URL2 = (j2).encode('utf-8')
            #print URL2.decode('utf-8')+'\n'
        print 'bazar breakpoint1'
        g = open( 'PATHTOTEMPTXTFILE', 'r' )
        if (any(re.findall(r'Продава', Zaglavie2, re.IGNORECASE))) and (2000 <= int(Cena2) <= 90000) and (any(re.findall(r'Младост', Kvartal2, re.IGNORECASE)) or any(re.findall(r'Младост', Zaglavie2, re.IGNORECASE))) and not (URL2 in g.read()):
            print 'bazar breakpoint2'
            g.close()
            g = open('PATHTOTEMPTXTFILE', 'a')
            print ("Заглавие: "+Zaglavie2).decode('utf-8')
            g.seek(0,2)
            g.write(Zaglavie2+'\n')
            print ("Квартал: "+Kvartal2).decode('utf-8')
            g.seek(0,2)
            g.write(Kvartal2+'\n')
            print ("Цена: "+str(Cena2)).decode('utf-8')
            g.seek(0,2)
            g.write(str(Cena2)+'\n')
            print ("URL: "+URL2+'\n').decode('utf-8')
            g.seek(0,2)
            g.write(URL2+'\n\n')
            g.close()
        
            #Send the mail
            headers2 = ("Message-ID: <"+str(random.randint(1000000000000000000000000000,9999999999999999999999999999))+"@mailer.DOMAIN.com>\nFrom: NAME1 <user@domain.com>\nTo: NAME2 <user2@domain2.com>\nSubject: "+Zaglavie2+'\nMIME-Version: 1.0\nContent-Type: text/html; charset=utf-8\nContent-Transfer-Encoding: 8bit\n')
            msg2 = ('\n\n<!DOCTYPE html><head><meta charset="UTF-8"></head><body><p style="margin-top:0in;margin-right:0in;margin-bottom:8.0pt;margin-left:0in;line-height:107%;font-size:15px;font-family:&quot;Calibri&quot;,sans-serif;">Заглавие - '+Zaglavie2+'<br>'+"Квартал - "+Kvartal2+'<br>'+"Цена - "+str(Cena2)+'<br>'+"URL - "+'<a href="'+URL2+'">'+URL2+'</a>'+'<br></p>'+'</body></html>\n\n')
        
            server.sendmail("MAILFROMADDRESS", ['MAILTOADDRESS1', 'MAILTOADDRESS2'], headers2+msg2)
            
#Bazar.bg
                
    server.quit
    print('Cycle done! '+str(datetime.datetime.now())[0:-7])
    for i in range(120):
       time.sleep(1)
