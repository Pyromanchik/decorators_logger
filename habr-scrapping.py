import requests
from bs4 import BeautifulSoup
from datetime import datetime

# === Декоратор logger для записи в файл ===
def logger(path):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            call_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            func_name = old_function.__name__
            args_str = ', '.join([repr(arg) for arg in args])
            kwargs_str = ', '.join([f"{k}={repr(v)}" for k, v in kwargs.items()])
            all_args = ', '.join(filter(None, [args_str, kwargs_str]))

            result = old_function(*args, **kwargs)

            log_message = f'{call_time} - {func_name}({all_args}) -> {result}\n'
            with open(path, 'a', encoding='utf-8') as log_file:
                log_file.write(log_message)

            return result
        return new_function
    return __logger


# Определяем список ключевых слов
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

# URL для парсинга
url = 'https://habr.com/ru/articles/'


@logger('habr.log')  # 🔹 Логируем эту функцию
def fetch_habr_articles():
    """
    Парсит страницу со свежими статьями на Хабре
    и возвращает список статей, содержащих ключевые слова
    """
    try:
        # Отправляем GET-запрос
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Создаем объект BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Находим все статьи на странице
        articles = soup.find_all('article', class_='tm-articles-list__item')

        matching_articles = []

        for article in articles:
            # Извлекаем заголовок и ссылку
            title_element = article.find('h2', class_='tm-title')
            if title_element:
                link_element = title_element.find('a')
                title = link_element.text.strip()
                link = 'https://habr.com' + link_element['href']
            else:
                continue

            # Извлекаем дату публикации
            time_element = article.find('time')
            if time_element:
                datetime_attr = time_element.get('datetime')
                if datetime_attr:
                    pub_date = datetime.fromisoformat(datetime_attr.replace('Z', '+00:00'))
                    date_str = pub_date.strftime('%Y-%m-%d %H:%M')
                else:
                    date_str = time_element.text.strip()
            else:
                date_str = 'Дата не указана'

            # Извлекаем preview-информацию
            preview_element = article.find('div', class_='article-formatted-body')
            if preview_element:
                preview_text = preview_element.text.strip()
            else:
                preview_element = article.find('div', class_='tm-article-body')
                preview_text = preview_element.text.strip() if preview_element else ''

            # Проверяем наличие ключевых слов
            found_keywords = []
            text_to_check = (title + ' ' + preview_text).lower()

            for keyword in KEYWORDS:
                if keyword.lower() in text_to_check:
                    found_keywords.append(keyword)

            if found_keywords:
                matching_articles.append({
                    'date': date_str,
                    'title': title,
                    'link': link,
                    'keywords': found_keywords
                })

        return matching_articles

    except requests.RequestException as e:
        print(f"Ошибка при запросе к сайту: {e}")
        return []
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return []


@logger('habr.log')  # 🔹 Логируем основную функцию
def main():
    """Основная функция программы"""
    print(f"Поиск статей по ключевым словам: {', '.join(KEYWORDS)}")
    print("-" * 60)

    articles = fetch_habr_articles()

    if articles:
        print(f"Найдено статей: {len(articles)}\n")
        for article in articles:
            print(f"{article['date']} – {article['title']} – {article['link']}")
            print(f"  Найдены ключевые слова: {', '.join(article['keywords'])}")
            print()
    else:
        print("Статьи с указанными ключевыми словами не найдены.")


if __name__ == "__main__":
    main()