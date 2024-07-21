class Book:
    ALLOW_STATUSES: tuple[str, ...] = ('в наличии', 'выдана')

    def __init__(self, title: str, author: str, year: int, id: int | None = None, status: str | None = None) -> None:
        self.title = title
        self.author = author
        self.year = year
        self.id = id
        self.status = status or self._in_stock_status()

    def __str__(self) -> str:
        return (
            f'ID - {self.id} | Название - {self.title} | Год - {self.year} | Автор - {self.author}\n'
            f'Статус - {self.status}'
        )

    def _in_stock_status(self) -> str:
        """Статус 'в наличии'."""
        return self.ALLOW_STATUSES[0]
