# python-crawler
本專案以Yahoo奇摩期貨產品為例，來源為 https://finance.yahoo.com/commodities  
使用開發Python網頁爬蟲取得關注的期貨當日行情，並且提供兩個方法(Method)，包含：
* Future_scrape()
* save()

其中，Future_scrape()方法為爬取關注的期貨當日行情，可自己選擇哪些產品，本專案選擇Gold、Silver、Crude Oil、Platinum、Palladium、Heating_Oil，
而save()方法提供存入MySQL資料庫的功能，以下為結果範例圖

![image](https://github.com/Eason0227/python-crawler/assets/102510341/ff2605b9-1abc-4cb5-ad73-722c14d24a58)

### reference
Beautiful Soup for Live Prices Using Python  
https://squatsstreak.medium.com/scraping-with-python-and-beautiful-soup-for-live-prices-2df75968ccd0  
[Python爬蟲教學]輕鬆學會Python網頁爬蟲與MySQL資料庫的整合方式  
https://www.learncodewithmike.com/2020/08/python-scraper-integrate-with-mysql.html  
Python 氣象資料爬蟲與MySQL資料庫實作  
https://www.youtube.com/watch?v=yWqJHDpbkPU  
