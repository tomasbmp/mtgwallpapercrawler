from urllib.request import urlopen
import urllib
import urllib.request
import re

base_url = "http://magic.wizards.com/en/see-more-wallpaper?page="
fim_url = "&filter_by=DESC&artist=-1&expansion&title"

global wpCount
global currentWP
global downloadLink
global currentFilepath
global currentRes
currentFilepath = ''
downloadLink = ''
currentWP = ''
currentRes = 0
wpCount = 0

basePath = "C:\\Users\\Tomas\\Pictures\\Wallpapers2\\"

def read(url):
    u = urlopen(url)
    contents = u.read()
    return contents.decode()

def readWpLinks(current_url):
    global currentWP
    global downloadLink
    global currentFilepath
    global currentRes
    global wpCount
    wallpapers = 0
    contents = read(current_url)
    links = re.findall('(?<=href=)(\S*\d+x\d+\S*.jpg)', contents)
    for link in links:
        link = re.sub('\\\\', '', link)
        link = re.sub('u0022', '', link)
        filename = re.sub('.*wallpaper/', '', link)
        filename = re.sub('_Wallpaper.*', '', filename)
        filename = re.sub('[-_]', ' ', filename)
        resolution = re.search('(\d+)x(\d+)', filename)
        filename = re.sub('\d+x\d+', '', filename)
        filename = re.sub('\d', '', filename)
        filename = re.sub('\....', '', filename)
        if currentWP != '' and filename != currentWP:
            print(str(wpCount) + ") " + currentFilepath)
            urllib.request.urlretrieve(downloadLink, currentFilepath)
            currentRes = 0
            wpCount += 1

        currentWP = filename
        width = resolution.group(1)
        height = resolution.group(2)
        if int(width)*int(height) > currentRes:
            currentRes = int(width)*int(height)
            downloadLink = link
            currentFilepath = basePath + filename + " " + resolution.group(0) + ".jpg"
    return int(re.search('"displaySeeMore":(\d)', contents).group(1))

i = 0
keep = 1
while(keep == 1):
    print(str(i) + "\n")
    url = base_url + str(i) + fim_url
    keep = readWpLinks(url)
    i = i+1
urllib.request.urlretrieve(downloadLink, currentFilepath)
print(str(wpCount) + ") " + currentFilepath)
