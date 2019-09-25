import requests
import re
import os
import pyfiglet
from pyfiglet import fonts
from colorama import Fore, Back, Style
from colorama import init
import time
import urllib3
from datetime import datetime



init()
# Console colors
W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple
C  = '\033[36m' # cyan
GR = '\033[37m' # gray
Y = '\033[93m'
BOLD = '\033[1m'
END = '\033[0m'

#Cookie of GET request https://www.okcupid.com/match
Cookie1 = ""

#Cookie and Authorization Token of POST request https://www.okcupid.com/1/apitun/messages/send
Cookie2 = ""
Authorization2 = ""

#Message
message = ''
payload_count = input("Enter the payload run count: ")


while True:
    try:

        
        regex = r"(\"userinfo\" : \{\"realname\" : \")([a-zA-Z\s\d\w]*)(\", \"gender_letter\" : \")([\w]*)(\", \"gender\" : \")([a-zA-Z]*)(\", \"age\" : )([\d]*)(, \"rel_status\" : \")([a-zA-Z]*)(\", \"location\" : \")([a-zA-Z\d\\]*)(\", \"orientation\" : \")([a-zA-Z]*)(\", \"displayname\" : \")([a-zA-Z\d\s]*)(\", \"staff_badge\" : [a-zA-Z]*}, \"last_login\" : [\d]*, \"likes\" : {\"mutual_like_vote\" : [\d]*, \"recycled\" : [\d]*, \"passed_on\" : [\d]*, \"they_like\" : [a-zA-Z]*, \"you_like\" : [a-zA-Z]*, \"via_spotlight\" : [a-zA-Z]*, \"mutual_like\" : [\d]*, \"vote\" : \{\}\}, \"percentages\" : \{\"match\" : )([\d]*)(, \"enemy\" : [\d]*}, \"inactive\" : [a-zA-Z]*, \"userid\" : \")([\d]*)(\", \"username\" : \")([\da-zA-Z]*)(\", \"staff\" : [a-zA-Z]*, \"thumbs\" : \[\{\"[\d]*x[\d]*\" : \")([a-zA-Z\d\/\:\.\_]*)"
        okcupiddata = open("okcupiddata.txt","a")
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        i = 0
        while i <= payload_count:

            headers = {
                "Host": "www.okcupid.com",
                "User-Agent": "MMozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0 Cyberfox/52.9.1",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "Cookie": Cookie1,
                "Connection": "close",
                "Upgrade-Insecure-Requests": "1"
            }

            url = "https://www.okcupid.com/match"
            #time.sleep(5)
            try:
                request = requests.get(url, headers=headers, verify=False)    
                response = (request.text.encode("utf-8"))
                temp = open("temp.txt","w")
                temp.write(response)
                temp.close()
            except:
                print "waiting for 20 sec.."
                time.sleep(20)
                continue
            temp_read = open ("temp.txt","r")
            contents = temp_read.readlines()
            for test_str in contents:
                matches = re.finditer(regex, test_str, re.MULTILINE)
                for matchNum, match in enumerate(matches, start=1):
                    details = match.group(2)+","+match.group(4)+","+match.group(6)+","+match.group(8)+","+match.group(10)+","+match.group(12)+","+match.group(14)+","+match.group(16)+","+match.group(18)+","+match.group(20)+","+match.group(22)+","+match.group(24)
                    userid = match.group(20)
                    
                    with open ('okcupiddata.txt','a+') as f:
                        if userid in f.read():
                            print R+"[+]"+END+GR+"Message already sent to "+END+match.group(2)
                        else:
                            print G+"[+]"+END+O+"Details Captured: "+END+match.group(2)+" "+match.group(8)+" "+match.group(12)+" "+match.group(18)+" "+match.group(20)+" "+match.group(22)+" "+match.group(24)
                            headers = {
                                "Host": "www.okcupid.com",
                                "User-Agent": "MMozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0 Cyberfox/52.9.1",
                                "Accept": "*/*",
                                "Accept-Language": "en-US,en;q=0.5",
                                "Accept-Encoding": "gzip, deflate",
                                "x-okcupid-platform": "DESKTOP",
                                "Authorization": Authorization2,
                                "Content-Type": "text/plain;charset=UTF-8",
                                "origin": "https://www.okcupid.com/",
                                "Referer": "https://www.okcupid.com/profile/"+userid+"?cf=regular,matchsearch",
                                "Cookie": Cookie2,
                                "Connection": "close"
                                }
                            now = datetime.now()
                            sendingtime = now.strftime("%d/%m/%Y %H:%M:%S")
                            print G+"[*]"+END+O+"["+sendingtime+"]"+END+O+"Sending Message To "+END+match.group(2)                            
                            #print message
                            postreq = '{"receiverid":"'+userid+'","body":"'+message+'","source":"desktop_global","service":"profile"}'
                            print postreq
                            url = "https://www.okcupid.com/1/apitun/messages/send"
                            time.sleep(5)
                            messagesend = requests.post(url, headers=headers, data=postreq, verify=False)
                            sendresponse = (messagesend.text.encode("utf-8"))
                            #print sendresponse
                            msgack = "success"
                            if msgack in sendresponse:
                                print G+"[+]"+END+O+"Message Sent Successfully to "+END+match.group(2)
                            else:
                                print sendresponse
                                print R+"[*]"+END+O+"Message Sending Failed"+END
                            print '..............................................................................................................'
                                
                            okcupiddata.write(details)
                            okcupiddata.write('\n')
            temp_read.close()
            os.remove("temp.txt")   
            i = i+1
            time.sleep(5)
            okcupiddata.close()
    except:
        print "Waiting for 10 Sec"
        time.sleep(10)
        headers = {
          "Host": "www.okcupid.com",
          "User-Agent": "MMozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0 Cyberfox/52.9.1",
          "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
          "Accept-Language": "en-US,en;q=0.5",
          "Accept-Encoding": "gzip, deflate",
          "Cookie": Cookie1,
          "Connection": "close",
          "Upgrade-Insecure-Requests": "1"
        }

        url = "https://www.okcupid.com/match"
        #time.sleep(5)
        request = requests.get(url, headers=headers, verify=False)    
        response = (request.text.encode("utf-8"))
        continue            
print ('\n')
print O+"Whooo!! Data Captured For Dating..."+END


