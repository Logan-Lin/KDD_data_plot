import time
import requests
from bs4 import BeautifulSoup
import re


now = time.time()
time_local = time.localtime(now)
dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
year = time.strftime('%Y', time_local)
month = time.strftime('%m', time_local)
day = time.strftime('%d', time_local)
hour = time.strftime('%H', time_local)
minute = time.strftime('%M', time_local)
second = time.strftime('%S', time_local)
raw_data = []

url = "https://www.tianqi.com/beijing/"
wbdata = requests.get(url).text
soup = BeautifulSoup(wbdata, 'html.parser')
news_titles = soup.select("dl.weather_info > dd")

pattern = re.compile(r"")

del news_titles[0:3]
for row in news_titles:
    for column in row:
        title = column.get_text()
        raw_data.append(title + '\r\n')  # 写入天气信息

        print(title)

raw_data.append(year + month + day + hour + minute + '\r\n')
print()
