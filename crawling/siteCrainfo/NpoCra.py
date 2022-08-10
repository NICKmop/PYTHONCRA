import requests;
from bs4 import BeautifulSoup;


# 번호로 페이지 이동
url = "https://www.snpo.kr/bbs/board.php?bo_table=bbs_npo&page=1";

response = requests.get(url); 
 
if response.status_code == 200:
    html = response.text;
    soup = BeautifulSoup(html, 'html.parser');

    content = soup.select('table.table > tr > td');

    Category = soup.select('table.table > tr > td.category');
    link = soup.select('table.table > tr >td > a');
    createUser = soup.select('table.table > tr > td:nth-child(3)');
    date = soup.select('table.table > tr > td.date');

    for i in range(len(createUser)):
        print("createUser : ", createUser[i].text.strip());
        print("Category : ", Category[i].text.strip());
        print("link : ", link[i].attrs.get('href'));
        print("date : ", date[i].text.strip());
 
