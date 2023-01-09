# Асинхронный парсер на Scrapy
Данный парсер предназначен для сбора информации об изменениях PEP и их колличестве с сайта https://peps.python.org/

Данный парсер на вывод формирует 3 файла (2 файла .csv и запись в БД(sqlite))
В файлах .csv содержиться информация о Номерах, названиях, и статусах PEP, а так же о их колличестве. В БД дублируется информация о Номерах, названиях, и статусах PEP.

## Подготовка к запуску проекта
Клонируем репозиторий:
git clone git@github.com:Vladimir-spb/scrapy_parser_pep.git
В клонированной дерриктории разворачиваем виртуальное окружение:
python -m venv venv
Устанавливаем зависимости:
pip install -r requirements.txt

## Запуск программы
scrapy crawl pep


После завершения работы формируется 3 файла:
- Список всех PEP с номерами и статусами (файл .csv) в дерриктории 'results/'
- Rоличество статусов и общее количество PEP (файл .csv) в дерриктории 'results/'
- БД sqlite со списком всех PEP с номерами и статусами в корневой дерриктории проекта.

## Автор:
Коршак Владимир 