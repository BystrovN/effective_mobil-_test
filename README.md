# Комментарии к тестовому заданию
1. Код соответствует pep8. Исключение - ограничение длины строки в 120 символов.
2. На реальном проекте следует вынести автора в отдельную сущность и изменить под это структуру и логику взаимодействия с БД. В рамках тестового задания считаю допустимым оставить автора просто строковым атрибутом у книги. 

# Приложение для управления библиотекой

Это консольное приложение для управления библиотекой. Позволяет добавлять, удалять, искать и отображать книги.

## Структура файлов
- main.py: Точка входа в приложение. Обрабатывает взаимодействие с пользователем и навигацию по меню.
- config.py: Содержит конфигурационные переменные для приложения.
- database.py: Определяет класс Database для работы с файлом JSON, который выступает в роли базы данных.
- objects/
    - library.py: Определяет класс Library для управления книгами в библиотеке.
    - book.py: Определяет класс Book, представляющий сущность книги.

## Запуск приложения

```
- python main.py
```

## Запуск тестов
```
- python test.py
```

## Использование
После запуска приложения будет предложено меню действий. Введите номер, соответствующий нужному действию.

### Варианты Меню
1. Добавить книгу
- Следуйте инструкциям для ввода названия, автора и года книги. Вводимые поля валидируются. При провале валидации будет предложено повторить ввод значения. 
- Книга будет добавлена в библиотеку, и вы увидите сообщение с подтверждением.

2. Удалить книгу
- Введите ID книги, которую хотите удалить.
- Если книга найдена, она будет удалена, и вы увидите сообщение с подтверждением.
- Если книга не найдена, вы увидите сообщение об ошибке.

3. Поиск
- Выберите поле для поиска (название, автор или год).
- Введите значение для поиска по выбранному полю.
- Будут отображены найденные книги. Если книги не найдены, вы увидите сообщение об ошибке.

4. Отобразить все книги
- Все книги в библиотеке будут отображены с подробной информацией.

5. Изменить статус книги
- Введите ID книги, статус которой хотите изменить.
- Введите новый статус (либо "в наличии", либо "выдана").
- Если книга найдена и статус корректный, статус будет обновлен, и вы увидите сообщение с подтверждением.
- Если книга не найдена или статус некорректный, вы увидите сообщение об ошибке.

6. Выйти
- Выход из приложения.

## Технологии
- Python - 3.11