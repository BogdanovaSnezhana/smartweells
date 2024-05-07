from fastapi import FastAPI
import uvicorn  # Здесь импортируем библиотку для запуска асинхронного сервера ( ASGI )

'''
Формула из xlsx файла для расчета объема
=0,785*POWER(B7;2)*B8
B7 это внутренний диаметр колонны ( column_inner_diameter ),
а B8 это глубина башмака колонны ( column_shoe_depth )
Пишем функцию для расчета объема
'''


def get_volume(column_inner_diameter, column_shoe_depth):  # Передаем параметры для формулы, которые в ней используются
    result = 0.785 * column_inner_diameter ** 2 * column_shoe_depth  # Считаем что получается по формуле
    return {'result': result}  # Возвращаем значение


'''
Для того чтобы работать с функциями, мы будем работать с API, который напишем сами
Для этого предлагаю использовать библиотку fastapi.

Для этого необходимо установить ее командой

- pip install fastapi

Либо же установить все из файла, в котором будет список всех нужных библиотек

- pip install -r requirements.txt
'''

'''
Для работы с либой напишем небольшой код
'''

app = FastAPI()

'''
Теперь переделаем нашу функцию для работы с api ( это пример, не обязательно, что именно эта функция нужна в api )
'''


@app.get('/get_volume/{column_inner_diameter}/{column_shoe_depth}')  # Это декоратор для получения GET запроса и создания эндпоинта
def get_volume(column_inner_diameter: float, column_shoe_depth: float):
    return 0.785 * column_inner_diameter ** 2 * column_shoe_depth


'''
Теперь запустим api сервер для того, чтобы проверить как работает эта функция
'''

if __name__ == '__main__':  # Этой строкой мы указываем питону, что этот файл является главным

    uvicorn.run('example:app', host='0.0.0.0', port=10000, reload=True)
    # Здесь мы запускает ASGI и говорим ему, что нам надо внутри файла example.py
    # найти переменную app и она является fastapi объектом,
    # потом указываем адрес устройства
    # (0.0.0.0 - это все доступные ip вашего устройства)
    # указываем порт на котором надо чтобы работал сервер
    # (10000 является примером, был так выбран
    # потому что у меня он свободен)
    # и просим постоянно перезагружаться при изменениях

'''
# После этого запускам наш python файл и в консоли должно выводить примерно такое сообщение

INFO:     Will watch for changes in these directories: ['/Users/maksimtimofeev/Work/Students/Example']
INFO:     Uvicorn running on http://0.0.0.0:10000 (Press CTRL+C to quit)
INFO:     Started reloader process [12088] using StatReload
INFO:     Started server process [12090]
INFO:     Waiting for application startup.
INFO:     Application startup complete.

Если перейти по ссылке которая написана в консоли и добавить в конец /docs
Получается во так:

- http://0.0.0.0:10000/docs

То можно будет увидеть все эндпоинты и попробовать с ними взаимодействовать
'''
