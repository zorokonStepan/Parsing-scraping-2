# для загрузки HTML кода страницы
import requests
# для нахождения элементов на странице используя CSS селекторы
from bs4 import BeautifulSoup
import sys
import json
import re


markets = {"iOS": "ios", "Google_Play": "google-play", "Amazon": "amazon-appstore", "Mac": "mac",
           "TV_Store": "appletv"}

country = {'australia': 'australia', 'austria': 'austria', 'belgium': 'belgium', 'brazil': 'brazil',
           'bulgaria': 'bulgaria', 'canada': 'canada', 'chile': 'chile', 'china': 'china', 'colombia': 'colombia',
           'croatia': 'croatia', 'czech-republic': 'czech-republic', 'denmark': 'denmark', 'ecuador': 'ecuador',
           'egypt': 'egypt', 'finland': 'finland', 'france': 'france', 'germany': 'germany', 'greece': 'greece',
           'hong-kong': 'hong-kong', 'hungary': 'hungary', 'india': 'india', 'indonesia': 'indonesia',
           'ireland': 'ireland',
           'israel': 'israel', 'italy': 'italy', 'japan': 'japan', 'kuwait': 'kuwait', 'lebanon': 'lebanon',
           'malaysia': 'malaysia', 'mexico': 'mexico', 'netherlands': 'netherlands', 'new-zealand': 'new-zealand',
           'norway': 'norway', 'pakistan': 'pakistan', 'peru': 'peru', 'philippines': 'philippines', 'poland': 'poland',
           'portugal': 'portugal', 'qatar': 'qatar', 'romania': 'romania', 'russia': 'russia',
           'saudi-arabia': 'saudi-arabia',
           'singapore': 'singapore', 'slovakia': 'slovakia', 'south-africa': 'south-africa',
           'south-korea': 'south-korea',
           'spain': 'spain', 'sweden': 'sweden', 'switzerland': 'switzerland', 'taiwan': 'taiwan',
           'thailand': 'thailand',
           'turkey': 'turkey', 'ukraine': 'ukraine', 'united-arab-emirate': 'united-arab-emirate',
           'united-kingdom': 'united-kingdom', 'united-states': 'united-states'}

categories = {"overall": "overall", 'games': 'games', 'applications': 'applications', 'books': 'books',
              'business': 'business', 'catalogs': 'catalogs', 'education': 'education',
              'entertainment': 'entertainment',
              'finance': 'finance', 'food-and-drink': 'food-and-drink', 'health-and-fitness': 'health-and-fitness',
              'kids': 'kids',
              'lifestyle': 'lifestyle', 'magazines-and-newspapers': 'magazines-and-newspapers', 'medical': 'medical',
              'music': 'music', 'navigation': 'navigation', 'news': 'news', 'photo-and-video': 'photo-and-video',
              'productivity': 'productivity', 'reference': 'reference', 'shopping': 'shopping',
              'social-networking': 'social-networking', 'sports': 'sports', 'travel': 'travel',
              'utilities': 'utilities',
              'weather': 'weather', 'developer-tools': 'developer-tools'}

device = {"iphone": "iphone", "ipad": "ipad"}

# ссылка на страницу для парсинга
if sys.argv[4] != "No":
    URL = f'https://www.appannie.com/ru/apps/{markets[sys.argv[1]]}/top/{country[sys.argv[2]]}/{categories[sys.argv[3]]}/{device[sys.argv[4]]}/'
else:
    URL = f'https://www.appannie.com/ru/apps/{markets[sys.argv[1]]}/top/{country[sys.argv[2]]}/{categories[sys.argv[3]]}/'
# HEADERS чтоб не заблокировали
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0',
           'accept': '*/*'}


def get_html(url, params=None):
    response = requests.get(url, headers=HEADERS, params=params)
    return response


def get_content(html):
    # sys.argv[5] == 'Бесплатно', 'Платные', 'Кассовые'
    soup = BeautifulSoup(html, 'html.parser')
    # открываем код который будем парсить, определенный столбец
    items = soup.find("div", class_="grid_15ty0v3-o_O-feedsGrid_j2lgag-o_O-layout_1w154zg-o_O-padding_sopvk0"). \
        find("h4", text=sys.argv[5]).find_previous().find_all("a")

    # запишем этот код в файл, чтоб лишний раз не обращаться к сайту
    with open("index8.html", "w", encoding='utf-8') as file:
        items = str(items)
        file.write(items)

    # открываем этот файл для парсинга данных
    with open("index8.html", encoding='utf-8') as file:
        src = file.read()
    soup_2 = BeautifulSoup(src, 'html.parser')

    # number_in_top - список по рейтингу
    number_in_top_1 = soup_2.find_all("p", class_='n_1jv8115-o_O-Small_7u8o3i-o_O-c8790a2_1bcd4jz-o_O-index_16g07o1')
    number_in_top = []
    for i in number_in_top_1:
        number_in_top.append(i.text)

    # application_name - список по названию приложения
    application_name_1 = soup_2.find_all("p",
                                         class_='n_1jv8115-o_O-Content_1xn1r0f-o_O-c0f2346_4s8r2l-o_O-text_7y41qf-o_O-item_9xo99e')
    application_name = []
    for i in application_name_1:
        application_name.append(i.text)

    # developers_name - список по названию разработчика
    developers_name_1 = soup_2.find_all("p", class_='n_1jv8115-o_O-Small_7u8o3i-o_O-c8790a2_1bcd4jz-o_O-item_9xo99e')
    developers_name = []
    for i in developers_name_1:
        developers_name.append(i.text)

    # link_on_the_website - список ссылок на приложение на сайте AppAnnie
    link_on_the_website_1 = soup_2.find_all("a", class_=re.compile('card_1o0ta6'))
    link_on_the_website = []
    for i in link_on_the_website_1:
        link_on_the_website.append(i.get('href'))

    result = []
    for count in range(len(number_in_top)):
        dict = {}
        dict["Позиция в топе"] = number_in_top[count]
        dict["Название приложения"] = application_name[count]
        dict["Название разработчика"] = developers_name[count]
        dict["Ссылка на приложение на сайте AppAnnie"] = "https://www.appannie.com" + link_on_the_website[count]
        dict["Рынок"] = sys.argv[1]
        dict["Страна"] = sys.argv[2]
        dict["Категория"] = sys.argv[3]
        dict["Устройство"] = sys.argv[4]
        dict["Столбец"] = sys.argv[5]
        result.append(dict)

    with open('answer.json', "w", encoding='utf-8') as data:
        data.write(json.dumps(result, ensure_ascii=False))


def parse():
    html = get_html(URL)
    # print(html.status_code)
    if html.status_code == 200:
        get_content(html.text)
    else:
        print('Error')


if __name__ == "__main__":
    parse()
