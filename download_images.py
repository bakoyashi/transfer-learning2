from urllib.request import urlretrieve
import os, sys, time, bs4, json
import urllib.request, urllib.error

# 設定：検索するキーワード
keywords = ['udon', 'pasta', 'ramen']

# 設定：検索する数
image_count = 50

# 設定：画像を保存するファイルパス
dataset_dir = "./dataset/"

def get_soup(url, header):
    return bs4.BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url,headers=header)),'html.parser')

def search_image(keyword):
    url="https://www.google.co.jp/search?q="+keyword+"&source=lnms&tbm=isch"
    header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
    soup = get_soup(url,header)
    return soup

def download_image(soup, save_directory):
    ActualImages=[]
    for a in soup.find_all("div",{"class":"rg_meta"}):
        link, Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
        ActualImages.append((link,Type))
    for i , (img , Type) in enumerate( ActualImages[0:image_count]):
        try:
            Type = Type if len(Type) > 0 else 'jpg'
            print("Downloading image {} ({}), type is {}".format(i, img, Type))
            raw_img = urllib.request.urlopen(img).read()
            f = open(os.path.join(save_directory , "img_"+str(i)+"."+Type), 'wb')
            f.write(raw_img)
            f.close()
        except Exception as e:
            print ("could not load : "+img)
            print (e)

# Googleから画像を保存する
for keyword in keywords:
    print("download now ...",  keyword)
    
    # 画像を保存するディレクトリを作成
    save_directory = "./dataset/" + keyword
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    
    # イメージ検索をする
    soup = search_image(keyword)

    # 画像をダウンロードする
    download_image(soup, save_directory)
