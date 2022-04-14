import time

import requests # 终端下载模块 pip install requests
import re
import os


#当文件夹不存在时创建这个文件夹
filename = 'music\\'
if not os.path.exists(filename):
    os.mkdir(filename)
#请求头
headers = {
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36 Edg/100.0.1185.36'
}

toplisturl = "https://music.163.com/discover/toplist"
rs = requests.get(toplisturl,headers=headers).text

toplist_url = re.findall('<a href="/discover/toplist\?id=(\d+)"(.*?)</a>',rs)


for toplist_id,toplist_name in toplist_url:
    toplist_name = toplist_name.replace(' class="s-fc0">','')
    print('当前榜单    '+toplist_name)
    url = f"https://music.163.com/discover/toplist?id={toplist_id}"
    response = requests.get(url,headers=headers)
    #正则表达式匹配response中的音乐Id和title
    html_data = re.findall('<li><a href="/song\?id=(\d+)">(.*?)</a></li>',response.text)

    for music_id,title in html_data:
        music_url = f"https://music.163.com/song/media/outer/url?id={music_id}.mp3" #网易云歌曲接口
        music_content = requests.get(url = music_url,headers=headers).content
        if '/' in title:
            title = title.replace('/','&')
        with open("music\\"+title+'.mp3','wb') as f:
            f.write(music_content)
        print(title+"     下载成功")
    print("爬取一个榜单后休息30秒")
    time.sleep(30)
