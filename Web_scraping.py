import requests
from bs4 import BeautifulSoup


def getdata(url):
    r = requests.get(url)
    print(r)
    return r.text

# htmldata = getdata("https://www.zillow.com/homedetails/479-Lee-Rd-SW-Mableton-GA-30126/97973628_zpid/")


htmldata = getdata("https://www.geeksforgeeks.org/data-science-with-python-tutorial/?ref=outind#machine-learning") 
soup = BeautifulSoup(htmldata, 'html.parser') 
res = soup.find_all("div", class_="is_h5-2 is_developer w-richtext") 
print(str(res))