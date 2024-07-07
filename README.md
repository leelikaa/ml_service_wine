# Реализация проекта и вопросы

## 14.04
1. реализованы базовые классы с учетом создания приложения на основе датасета и модели про качество вина.
2. добавлены предварительные связи (без реализации еще сложно понять, будет дорабатываться)

## 01.07
попытка добавления докера. Есть вопрос в части "склейки" с уже наработанной структурой. 

## 07.07
реализвала подключение к БД и тест создания пользователей и транзакций, но возникла проблема (ниже пример выдаваемых логов). Не очень понимаю где я косячу: из ошибок следует, что id транзакций не создаются, хотя в schema.py я прописывала это поле c primary_key=True. с юзером тоже странно, так как их id точно есть...

```
[+] Running 2/0
 ✔ Container db                  Running                                          0.0s
 ✔ Container wine_project-app-1  Created                                          0.0s
Attaching to db, app-1
app-1  | /usr/local/lib/python3.11/site-packages/pydantic/_internal/_config.py:341: UserWarning: Valid config keys have changed in V2:
app-1  | * 'orm_mode' has been renamed to 'from_attributes'
app-1  |   warnings.warn(message, UserWarning)
app-1  | Traceback (most recent call last):
app-1  |   File "/app/main.py", line 22, in <module>
app-1  | Init db has been success
app-1  | [<model.users.Users object at 0x7ff21b1b3710>, <model.users.Users object at 0x7ff21b1b3790>, <model.users.Users object at 0x7ff21c15d0d0>, <model.users.Users object at 0x7ff21e762990>]
app-1  | id: 1 - test1@mail.ru
app-1  | id: 2 - test2@mail.ru
app-1  | id: 3 - test1@mail.ru
app-1  | id: 4 - test2@mail.ru
app-1  |     top_up(1, 10.0, session)
app-1  |   File "/app/services/Transaction_Services.py", line 37, in top_up
app-1  |     transaction = Transaction(user_id=user_id, time=datetime.now(), money=money, type_="top-up")
app-1  |                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
app-1  |   File "/usr/local/lib/python3.11/site-packages/pydantic/main.py", line 193, in __init__
app-1  |     self.__pydantic_validator__.validate_python(data, self_instance=self)
app-1  | pydantic_core._pydantic_core.ValidationError: 2 validation errors for Transaction
app-1  | transaction_id
app-1  |   Field required [type=missing, input_value={'user_id': 1, 'time': da...10.0, 'type_': 'top-up'}, input_type=dict]
app-1  |     For further information visit https://errors.pydantic.dev/2.8/v/missing
app-1  | user
app-1  |   Field required [type=missing, input_value={'user_id': 1, 'time': da...10.0, 'type_': 'top-up'}, input_type=dict]
app-1  |     For further information visit https://errors.pydantic.dev/2.8/v/missing
app-1 exited with code 1
```

