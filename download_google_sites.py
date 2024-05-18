import requests
from bs4 import BeautifulSoup
import os

def download_google_sites_content(url, output_file, assets_dir):
    """
    下载 Google Sites 内容、图片和删除重定向语句，保存到本地文件。

    参数：
        url (str): Google Sites 页面 URL。
        output_file (str): 输出 HTML 文件的路径。
        assets_dir (str): 图片存放的文件夹路径。
    """
    response = requests.get(url)
    response.raise_for_status()  # 检查 HTTP 状态码

    soup = BeautifulSoup(response.content, 'html.parser')

    # 删除所有 meta 标签中的 refresh 属性
    for meta in soup.find_all('meta', {'http-equiv': 'refresh'}):
        meta.decompose()

    # 删除所有 script 标签中的重定向代码
    for script in soup.find_all('script'):
        if 'location.href' in script.text:
            script.decompose()

    # 下载图片
    for img in soup.find_all('img'):
        img_src = img['src']
        if img_src.startswith('http'):
            img_filename = img_src.split('/')[-1]
            img_path = os.path.join(assets_dir, img_filename)
            try:
                with open(img_path, 'wb') as f:
                    img_response = requests.get(img_src)
                    img_response.raise_for_status()
                    f.write(img_response.content)
                img['src'] = f'/assets/{img_filename}'  # 更新图片路径
            except Exception as e:
                print(f"下载图片失败：{img_src}, 错误信息：{e}")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(str(soup))

if __name__ == '__main__':
    google_sites_url = 'https://sites.google.com/view/jianwangfudan'
    output_html_file = 'index.html'
    assets_dir = '.'  # 图片存放的文件夹路径
    download_google_sites_content(google_sites_url, output_html_file, assets_dir)
