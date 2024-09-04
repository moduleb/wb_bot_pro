#
#### Адрес сервера
Приложение доступно по адресу:  
- на локальной машине `http://localhost/`  
- на удаленном сервере `http://<IP адрес сервера>`  
- `/docs` - документация Swagger  


#### CREATE
<a id="create"></a>
**[post]** .../api/v1/items

Принимает JSON с данными нового товара:
```json
{
  "url": "string", # ссылка на товар
  "user_id": "string" # id пользователя в телеграм
}
```

Возвращает `201 CREATED`

---

#### GET ALL
<a id="get_all"></a>
**[get]** .../api/v1/items
Параметры:  
 - `user_id`: integer

Возвращает все добавленные товары для заданного пользователя:
```json
[
    {
        "id": 8,
        "user_id": 5312665858,
        "item_id": 176656692,
        "price": 1753,
        "title": "Педали для велосипеда на трех промышленных подшипниках",
        "url": "https://www.wildberries.ru/catalog/176656692/detail.aspx"
    },
    {
        "id": 9,
        "user_id": 5312665858,
        "item_id": 165835462,
        "price": 1338,
        "title": "Багажник на велосипед",
        "url": "https://www.wildberries.ru/catalog/165835462/detail.aspx"
    }
]
```

---

#### DELETE
<a id="delete"></a>
**[delete]** .../api/v1/items
Параметры:  
 - `user_id`: integer  
 - `item_id`: integer

Возвращает `204 NO CONTENT`



