import requests
from bs4 import BeautifulSoup as Bs
from utility import data_regularization as dr


url = "https://www.tianqi.com/beijing/30/"
text = requests.get(url).text
soup = Bs(text, 'html.parser')
temp_matrix = []
wind_raw_string = []
for day in soup.find_all("div", {"class": "table_day"}):
    all_data = day.find_all("li")
    for i in range(1, len(all_data), 2):
        temp_matrix.append(dr.get_temp_scope(all_data[i].text))
    for i in range(2, len(all_data), 2):
        wind_raw_string.append(all_data[i].text)
print(temp_matrix)
print(wind_raw_string)
