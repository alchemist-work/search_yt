import sys, getopt,requests,re,json,time,ast,random,string
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
suglist = []
suglist6 = []


def rstr(count):
  return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(count))


def filtersub(content,path,tt):
  rr = re.findall("var ytInitialData = {\"responseContext\"[^\r\n]{0,}};</script><script",content)
  if len(rr)<=0:
    #print("error")
    return
  jc = json.loads(rr[0][20:-17])
  cc = (jc['header']['pageHeaderRenderer']['content']['pageHeaderViewModel']['metadata']['contentMetadataViewModel']['metadataRows'][1]['metadataParts'][0]['text']['content'])
  cn = cc.replace(',','').replace("subscribers",'')
  if "K" in cn:
    return str(float(cn.replace('K',''))*1000)
  if "M" in cn:
    return str(float(cn.replace('M',''))*1000000)
  else:
    return cn
def getsub(path,tt):
  url = "https://www.youtube.com"+path+"?sttick=0"
  r6 = rstr(6)
  r9 = rstr(9)
  r20 = rstr(20)
  r43 = rstr(43)
  r66 = rstr(66)
  headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-US,en;q=0.9",
    "priority": "u=0, i",
    "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
    "sec-ch-ua-arch": "\"x86\"",
    "sec-ch-ua-bitness": "\"64\"",
    "sec-ch-ua-form-factors": "\"Desktop\"",
    "sec-ch-ua-full-version": "\"132.0.6834.160\"",
    "sec-ch-ua-full-version-list": "\"Not A(Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"132.0.6834.160\", \"Google Chrome\";v=\"132.0.6834.160\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-model": "\"\"",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-ch-ua-platform-version": "\"15.2.0\"",
    "sec-ch-ua-wow64": "?0",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "service-worker-navigation-preload": "true",
    "upgrade-insecure-requests": "1",
    "x-browser-channel": "stable",
    "x-browser-copyright": "Copyright 2025 Google LLC. All rights reserved.",
    "x-browser-validation": f"{r20}+{r6}=",
    "x-browser-year": "2025",
    "x-client-data": f"{r43}+{r66}/{r9}"
  }
  ret = requests.get(url = url,headers=headers,verify = False,proxies=None)
  return filtersub(ret.text,path,tt)

def searchwd(wd):
  baseurl = "https://www.youtube.com/results?search_query="
  r6 = rstr(6)
  r9 = rstr(9)
  r20 = rstr(20)
  r43 = rstr(43)
  r66 = rstr(66)
  headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "priority": "u=0, i",
    "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
    "sec-ch-ua-arch": "\"x86\"",
    "sec-ch-ua-bitness": "\"64\"",
    "sec-ch-ua-form-factors": "\"Desktop\"",
    "sec-ch-ua-full-version": "\"132.0.6834.160\"",
    "sec-ch-ua-full-version-list": "\"Not A(Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"132.0.6834.160\", \"Google Chrome\";v=\"132.0.6834.160\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-model": "\"\"",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-ch-ua-platform-version": "\"15.2.0\"",
    "sec-ch-ua-wow64": "?0",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "service-worker-navigation-preload": "true",
    "upgrade-insecure-requests": "1",
    "x-browser-channel": "stable",
    "x-browser-copyright": "Copyright 2025 Google LLC. All rights reserved.",
    "x-browser-validation": f"{r20}+{r6}=",
    "x-browser-year": "2025",
    "x-client-data": f"{r43}+{r66}/{r9}"}
  try:
    ret = requests.get(url = baseurl+wd,headers=headers,verify = False,proxies=None)
    #print(ret.status_code)
    if ret.status_code==200:
      return ret.text
  except Exception as e:
    return

def filter(content,wd):
  #print(content)
  if content == None:
    print("None!\n")
    return
  #var ytInitialData = {"responseContext"
  #"};</script><script
  rr = re.findall("var ytInitialData = {\"responseContext\"[^\r\n]{0,}};</script><script",content)
  #print(type(rr))
  #print(len(rr))
  #print((rr[0][39:-17]))
  #print(len(rr))
  if len(rr)<=0:
    #print("error")
    return
  jc = json.loads(rr[0][20:-17])
  tt = str(time.time())
  #fp = open(jname,"w+")
  #fp.write(json.dumps(jc,indent = 2))
  #fp.close()
  #print(jc['estimatedResults'])

  if "refinements" in jc:
    global suglist
    suglist = jc['refinements']
  user = []
  print(wd+","+jc['estimatedResults']+" Results")
  return
  js = jc['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']
  for i in js:
    try:
        if "videoRenderer" in i:
          pa = i['videoRenderer']['avatar']['decoratedAvatarViewModel']['rendererContext']['commandContext']['onTap']['innertubeCommand']['commandMetadata']['webCommandMetadata']['url']
          sub = int(float(getsub(pa,tt)))
          #time.sleep()
          volum = jc['estimatedResults']
          t = i['videoRenderer']['title']['runs'][0]['text']
          ptime = i['videoRenderer']['publishedTimeText']['simpleText'].replace(',','')
          viewcount = i['videoRenderer']['viewCountText']['simpleText'].replace(',','')
          authurl = i['videoRenderer']['avatar']['decoratedAvatarViewModel']['rendererContext']['commandContext']['onTap']['innertubeCommand']['commandMetadata']['webCommandMetadata']['url']
          longtxt = i['videoRenderer']['lengthText']['accessibility']['accessibilityData']['label']
          videolink = i['videoRenderer']['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']
          #auth = i['videoRenderer']['ownerText']['runs'][0]['text']
          rate = (float(viewcount.replace("views",''))/(sub))*100
          row =str(int(rate))+"%"+","+wd+","+volum+","+viewcount+","+str(sub)+","+ptime+","+longtxt+","+videolink
          log = str(int(rate))+"%"+","+wd+","+volum+","+viewcount+","+str(sub)+","+ptime
          if "year" not in ptime and rate>1000:
            if "/shorts" in videolink:
              print("shorts:"+log)
            else:
              pass
              #print("videos:"+log)
    except Exception as e:
      continue
    

def sug6(wd):
  try:
    r42 = rstr(42)
    url = f"https://suggestqueries-clients6.youtube.com/complete/search?ds=yt&hl=en&gl=us&client=youtube&gs_ri=youtube&gs_id=2&q={wd}&cp=2"
    headers = {
    "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
    "sec-ch-ua-arch": "\"x86\"",
    "sec-ch-ua-bitness": "\"64\"",
    "sec-ch-ua-form-factors": "\"Desktop\"",
    "sec-ch-ua-full-version": "\"132.0.6834.160\"",
    "sec-ch-ua-full-version-list": "\"Not A(Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"132.0.6834.160\", \"Google Chrome\";v=\"132.0.6834.160\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-model": "\"\"",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-ch-ua-platform-version": "\"15.2.0\"",
    "sec-ch-ua-wow64": "?0",
    "x-goog-visitor-id": f"{r42}%3D%3D",
    "referrer": "https://www.youtube.com/",
    "referrerPolicy": "origin-when-cross-origin",
    "body": "null",
    "method": "GET",
    "mode": "cors",
    "credentials": "omit"
    }
    ret = requests.get(url=url,headers=headers,verify=False)
    tt = re.findall(r'window.google.ac.h\([^\r\n]{1,}',ret.text)
    x = ast.literal_eval(tt[0][19:-1])
    for i in x[1]:
      global suglist6
      suglist6.append(i[0])
  except Exception as e:
    return

def dig(wd):
  time.sleep(3)
  sug6(wd)
  #print(suglist6)
  for i in suglist6:
    #time.sleep(3)
    filter(searchwd(i),i)
    for j in set(suglist):
      #time.sleep(3)
      filter(searchwd(j),j)

#keywords-pickaxe
#KRT-pickaxe

def main():
  dig("find keyword volum")

if __name__ == '__main__':
	main()