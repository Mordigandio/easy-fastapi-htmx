class BookAlreadyExistsError(Exception):
    """ cst-ошибка """
    def __init__(self, title: str, author: str):
        self.message = f"Книга '{title}' от '{author}' уже есть в базе."
        super().__init__(self.message)