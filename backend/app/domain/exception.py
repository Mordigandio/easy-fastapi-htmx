from fastapi import status


class DomainError(Exception):
    """ Базовое исключение доменного слоя """

    status_code: int = status.HTTP_400_BAD_REQUEST
    message: str = "ERRRRR"

class BookAlreadyExistsError(DomainError):
    """ Ошибка существующей книги """

    status_code = status.HTTP_409_CONFLICT

    def __init__(self, title: str, author: str):
        self.message = f"Книга '{title}' от автора '{author}' уже существует."


class BookNotFoundError(DomainError):
    """ Ошибка отсутствующей книги """
    
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, book_id: int):
        self.message = f"Книга с ID {book_id} не найдена"
