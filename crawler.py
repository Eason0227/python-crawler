from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime
import pymysql

class Future:
    def __init__(self, select_product):
        self.select_product = select_product
    
    def Future_scrape(self):
        today = datetime.date.today()
        formatted_date = today.strftime("%Y-%m-%d")

        CommoditiesUrl = "https://finance.yahoo.com/commodities"
        r= requests.get(CommoditiesUrl, features="lxml")
    
        data=r.text
        soup=BeautifulSoup(data)

        prices=[]
        names=[]
        changes=[]
        percentChanges=[]
        marketTimes=[]
        totalVolumes=[]
        openInterests=[]
        date = [] 
        for row in soup.find_all('tbody'):
            for srow in row.find_all('tr'):
                for name in srow.find_all('td', attrs={"aria-label":"Name"}):
                    names.append(name.text)
                for price in srow.find_all('td', attrs={"aria-label":"Last Price"}):
                    prices.append(price.text)
                for time in srow.find_all('td', attrs={"aria-label":"Market Time"}):
                    marketTimes.append(time.text)
                for change in srow.find_all('td', attrs={"aria-label":"Change"}):
                    changes.append(change.text)
                for percentChange in srow.find_all('td', attrs={"aria-label":"% Change"}):
                    percentChanges.append(percentChange.text)
                for volume in srow.find_all('td', attrs={"aria-label":"Volume"}):
                    totalVolumes.append(volume.text)
                for openInterest in srow.find_all('td', attrs={"class":"Va(m) Ta(end) Pstart(20px) Pend(10px) W(120px) Fz(s)"}):
                    openInterests.append(openInterest.text)
                date.append(formatted_date)

        commodities = pd.DataFrame({'date' : date,"Names": names, "Prices": prices, "Change": changes, "% Change": percentChanges, "Market Time": marketTimes,'Open Interest': openInterests ,"Volume": totalVolumes})
        #  several duplicates on the scraped dataframe
        commodities.drop_duplicates(subset ="Names", keep = "first", inplace = True)
        # set the names as Index
        commodities = commodities.set_index('Names')
        # rename some of the Names
        commodities.rename(index= {"Platinum Jan 24": "Platinum ", # 柏金
                                    "Copper Dec 23":"Copper",
                                    "Palladium Dec 23":"Palladium", # 鈀金
                                    "Heating Oil Dec 23":"Heating_Oil",
                                    "Natural Gas Dec 23":"Natural Gas",
                                    "RBOB Gasoline Dec 23":"RBOB Gasoline",
                                    "Cocoa Mar 24":"Cocoa",
                                    "Coffee Mar 24":"Coffee",
                                    "Cotton Mar 24":"Cotton",
                                    "Orange Juice Jan 24":"Orange",
                                    "Sugar #11 Mar 24":"Sugar"},inplace = True)
        commodities.insert(1,'Name',commodities.index)

        result = []
        for i in self.select_product:
            result.append(tuple( commodities.loc[i].values ))
        return result

    def save(self, numbers):
        db_settings = {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "password": "assd40393",
        "db": "crawler",
        "charset": "utf8"
        }
        try:
            conn = pymysql.connect(**db_settings)
            with conn.cursor() as cursor:
                sql = "INSERT INTO product_data(market_date,Name,prices,change_value,change_rate,Market_Time,open_interest,volume)VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
                for number in numbers:
                    cursor.execute(sql, number)
                    conn.commit()
        
        except Exception as ex:
            print("Exception:", ex)

select_product = ['Gold','Silver','Crude Oil','Platinum ','Palladium','Heating_Oil']
future = Future(select_product)
future.save(future.Future_scrape())