import requests, lxml, time
from bs4 import BeautifulSoup


URL = 'https://habr.com/ru/all/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
           'accept': '*/*'}
keywords = {'дизайн', 'фото', 'web', 'python *', 'python', 'tele2', 'aстрономия', 'c++'}


def habr_info():

    info = {}
    habr = requests.get(url=URL, headers=HEADERS)

    if habr.status_code != 200:
        print('Habr не доступен! Проверьте подключение, или попробуйте позже.')
    else:
        soup = BeautifulSoup(habr.content, 'html.parser')
        pre_post = soup.select("article")

        for i in pre_post:
            date = i.find('time').get('title')
            title = i.find(class_="tm-article-snippet__title-link").text
            link = 'https://habr.com' + i.find(class_="tm-article-snippet__title-link").get('href')
            hubs = i.find_all(class_="tm-article-snippet__hubs-item-link")
            hubs = {h.text.strip().lower() for h in hubs}
            post = requests.get(url=link, headers=HEADERS)

            if post.status_code != 200:
                print(f'Страница статьи {title} не доступна.')
            else:
                soup_post = BeautifulSoup(post.content, 'lxml')
                text_post = soup_post.find(id="post-content-body").text

                for word in keywords:

                    if word in text_post:
                        info[date] = [f"[{title}]({link})", word]

                    if hubs & keywords:
                        hub = []
                        for _ in hubs:
                            if "*" in _:
                                hub.append(_.replace("*", "\*"))
                        info[date] = [f"[{title}]({link})", ' | '.join(hub)]

    return info


def new_post():
    post = habr_info()
    posts = []
    for date, post_info in post.items():
        posts.append(f"{date} - {' | '.join(post_info)}")

    return(posts)


if __name__ == '__main__':
    posts = new_post()
    for i in posts:
        print(i)
