import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "https://www.iplt20.com/auction"
r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")

table = soup.find("table", class_="ih-td-tab auction-tbl")
header = table.find_all("th")
titles = [i.text for i in header]

df = pd.DataFrame(columns=titles)

data = table.find_all("tr")
for i in data[1:]:
    columns = i.find_all("td")

    if len(columns) > 1:
        team = columns[0].text.strip()
        first_td = columns[1].find("div", class_="ih-pt-ic")

        if first_td:
            first_td_text = first_td.text.strip()
        else:
            first_td_text = ""

        rows = columns[1:]
        row = [tr.text for tr in rows]
        row.insert(0, first_td_text)
        l = len(df)
        df.loc[l] = row

        # Print the extracted data
        print(f"Team: {team}, Player: {first_td_text}, Data: {row}")

df.to_csv("IPL_Auction_Status_2020.csv", index=False)
