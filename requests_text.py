import requests
from bs4 import BeautifulSoup
import os


class meizitu():
    def all_url(self,start_url):
        self.find_photos(start_url)
         ##去掉空格

        # os.chdir('E:\mzitu\\' + path)  ##切换到上面创建的文件夹\\表示第二个\为\，而不是转义符


    def find_photos(self,start_url):
        start_html = self.request(start_url)
        Soup = BeautifulSoup(start_html.text, 'lxml')
        max_page = Soup.find('div', class_='nav-links').find_all('a')[-2].get_text()
        for main_page in range(1, int(max_page) + 1):  #从主站遍历所有
            main_page_url = start_url + '/page' + str(main_page)
            main_page = self.request(main_page_url)  ##下一页
            main_soup = BeautifulSoup(main_page.text, 'lxml')
            all_a = main_soup.find('ul', id='pins').find_all('a')  ##链接
            c = 1
            for a in range(0, 24):         #遍历每一页图片
                title = all_a[c].get_text()  # 取出标签文本
                href = all_a[c]['href']
                path = str(title).strip()
                html = self.request(href)
                html_soup = BeautifulSoup(html.text, 'lxml')
                max_span = html_soup.find('div', class_='pagenavi').find_all('span')[-2].get_text()
                if self.mkdir(path):  # 创建文件夹
                    for page in range(1, int(max_span) + 1):
                        page_url = href + '/' + str(page)
                        self.img(page_url)
                c = c + 2

    def img(self, page_url):  # 获得每一页的图片
        img_html = self.request(page_url)
        img_Soup = BeautifulSoup(img_html.text, 'lxml')
        img_url = img_Soup.find('div', class_='main-image').find('img')['src']
        self.save(img_url)

    def save(self,img_url):
        name = img_url[-9:-4]  ##取URL 倒数第四至第九位 做图片的名字
        img = self.request(img_url)
        f = open(name + '.jpg', 'ab')
        f.write(img.content)
        f.close()

    def mkdir(self,path):
        path=path.replace('?','_')
        isExists=os.path.exists(os.path.join("E:\mzitu",path))
        if not isExists:
            print(u'开始保存：', path)
            print('创建了一个',path,'的文件夹')
            os.makedirs(os.path.join('E:\mzitu', path))  ##创建一个存放套图的文件夹
            os.chdir(os.path.join('E:\mzitu', path))
            return True
        else:
            print('名字为',path,'的文件夹已经存在了')
            return False



    def request(self,url):
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
        content = requests.get(url, headers=headers)
        return content


#all_url = 'http://www.mzitu.com/'





Meizi=meizitu()
Meizi.all_url('http://www.mzitu.com/')