import requests
from bs4 import BeautifulSoup
import pandas as pd
from httpcache import CachingHTTPAdapter
# Import dataframe into MySQL
import sqlalchemy

s = requests.Session()
s.mount('http://', CachingHTTPAdapter())
s.mount('https://', CachingHTTPAdapter())
infoLinks = []
baseurl = 'https://webscraper.io/'
for i in range(1, 21):
    page = requests.get(f'https://webscraper.io/test-sites/e-commerce/static/computers/laptops?page={i}')
    soup = BeautifulSoup(page.content, 'lxml')
    divContent = soup.find('div', class_="col-md-9")
    infoList = divContent.find_all('div', class_="thumbnail")
    for product in infoList:
        infoLinks.append(baseurl + product.find_all('h4')[-1].find('a')['href'])
    print(f'Visiting Page - {i}')

productsInfo = []
for link in infoLinks:
    productPage = requests.get(link)
    soup = BeautifulSoup(productPage.content, 'lxml')
    productCaption = soup.find_all('h4')
    productName = productCaption[-1].text
    productPrice = productCaption[0].text
    productDesc = soup.find('p', class_='description').text
    productReviews = soup.find('div', class_="ratings").find('p').text.strip()
    productRatings = len(soup.find('div', class_="ratings").find_all('span'))
    product = {
        "name": productName,
        "price": productPrice,
        "description": productDesc,
        "ratings": productRatings,
        "reviews": productReviews
    }
    productsInfo.append(product)
    print(f'Saving product- {productName}')

print(f'Total Products crawled - {len(productsInfo)}')
productDataframe = pd.DataFrame(productsInfo)
file_name = 'productData.xlsx'

# saving the excel
productDataframe.to_excel(file_name)
print(f'Data saved to excel file name- {file_name}')



database_username = 'root'
database_password = 'ankit8317'
database_ip       = 'localhost'
database_name     = 'eCommerce'
database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(database_username, database_password,
                                                      database_ip, database_name))
productDataframe.to_sql(con=database_connection, name='computers', if_exists='replace')