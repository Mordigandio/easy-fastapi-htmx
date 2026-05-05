from app.dependencies.deps import BookRepoDeps
from app.schemas.book import BookCreate, BookResponse, BookUpdate
from fastapi import APIRouter, HTTPException, Response, status

router = APIRouter(prefix="/books", tags=["books"])

@router.post(
    "/", 
    response_model=BookResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Создать новую книгу",
    description="Принимает данные книги и сохраняет их в базу данных. Возвращает созданную запись с ID."
    )
async def create_book(
    book_data: BookCreate,
    repo: BookRepoDeps
    ):
    book = await repo.create(book_data)
    return book

@router.get(
    "/",
    response_model=list[BookResponse],
    summary="Получить список книг",
    description="Возвращает список всех книг с поддержкой пагинации (skip и limit). Сортировка по дате создания (новые сверху)."
    )
async def list_books(
    repo: BookRepoDeps,
    skip: int = 0,
    limit: int = 100
    ):
    books = await repo.list(skip=skip, limit=limit)
    return books

@router.get(
    "/{book_id}",
    response_model=BookResponse,
    summary="Получить информацию о книге",
    description="Возвращает детальные данные конкретной книги по её уникальному идентификатору (ID)."
    )
async def get_book(
    book_id: int,
    repo: BookRepoDeps
    ):
    book = await repo.get(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return book

@router.patch(
    "/{book_id}",
    response_model=BookResponse,
    summary="Частично обновить книгу",
    description="Обновляет только те поля книги, которые были переданы в теле запроса. Если книга не найдена — 404."
    )
async def update_book(
    book_id: int,
    book_data: BookUpdate,
    repo: BookRepoDeps
    ):
    book = await repo.update(book_id, book_data)
    if book is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return book

@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить книгу",
    description="Навсегда удаляет запись о книге из базы данных. Возвращает пустой ответ в случае успеха."
    )
async def delete_book(
    book_id: int,
    repo: BookRepoDeps
    ):
    success = await repo.delete(book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return Response(status_code=status.HTTP_204_NO_CONTENT)