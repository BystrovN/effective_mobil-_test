import json
import os
import uuid
from typing import TypeVar, Generic

T = TypeVar('T', bound=dict[str, str | int])


class Database(Generic[T]):
    """Класс Database для работы с файлом JSON как с БД."""

    ID_FIELD = 'id'

    def __init__(self, file_name: str):
        self.file_name = file_name
        self.data: list[T] = self._load_data()

    def _load_data(self) -> list[T]:
        """Загрузка всех данных."""
        if not os.path.exists(self.file_name):
            return []

        try:
            with open(self.file_name, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_data(self) -> None:
        """Сохранение данных."""
        with open(self.file_name, 'w') as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)

    def _set_id(self, instance: T) -> None:
        """Установка id сущности при его отсутствии."""
        if instance.get(self.ID_FIELD):
            return

        instance[self.ID_FIELD] = self.id_generator()

    def id_generator(self) -> str:
        """Генератор уникального id в виде случайной строки из 16 символов."""
        id = uuid.uuid4().hex[:4]

        return id if not self.find_by(self.ID_FIELD, id) else self.id_generator()

    def find_by(self, field: str, value: str | int) -> list[dict[str, str | int]]:
        """Поиск записи по переданному полю."""
        return [instance for instance in self.data if instance.get(field) == value]

    def append_data(self, instance: T) -> None:
        """Добавление данных."""
        self._set_id(instance)
        self.data.append(instance)
        self._save_data()

    def delete_data_by_id(self, id: int | str) -> None:
        """Удаление данных по id."""
        self.data = [instance for instance in self.data if instance.get(self.ID_FIELD) != id]
        self._save_data()

    def update_data(self, instance: T) -> None:
        """Обновление данных экземпляра."""
        if instance.get(self.ID_FIELD) is None:
            return

        self.delete_data_by_id(instance[self.ID_FIELD])
        self.append_data(instance)
