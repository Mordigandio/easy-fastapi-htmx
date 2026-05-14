from typing import Annotated

from app.dependencies.deps import BookRepoDeps
from app.schemas.book import BookCreate, BookUpdate
from app.utils.templates import templates
from fastapi import APIRouter, Form, HTTPException, Request, Response, status
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/books", tags=["books"])

@router.post(
    "/", 
    response_class=HTMLResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Создать новую книгу",
    description="Принимает данные книги через форму и сохраняет их в базу данных. Возвращает карточку созданной книги."
)
async def create_book(
    request: Request,
    response: Response,
    repo: BookRepoDeps,
    book_data: Annotated[BookCreate, Form()],
):
    new_book = await repo.create(book_data)
    response.headers["HX-Trigger"] = "closeModal"
    
    return templates.TemplateResponse(
        request=request, 
        name="book_card.html", 
        context={"book": new_book}
    )

@router.get(
    "/",
    response_class=HTMLResponse,
    summary="Получить список книг",
    description="Возвращает список всех книг с фильтрацией, поиском и поддержкой пагинации"
)
async def list_books(
    request: Request,
    repo: BookRepoDeps,
    skip: int = 0,
    limit: int = 100,
    search: str | None = None,
    author: str | None = None,
    book_id: str | None = None
):
    # получение списка книг по параметрам
    if book_id and book_id.isdigit():
        book = await repo.get(int(book_id))
        books = [book] if book else []
    elif search or author:
        books = await repo.list(skip=skip, limit=limit, search=search or author)
    else:
        books = await repo.list(skip=skip, limit=limit)

    return templates.TemplateResponse(
        request=request,
        name="books_list.html",
        context={"books": books}
    )

@router.patch(
    "/",
    response_class=HTMLResponse,
    summary="Частично обновить книгу",
    description="Обновляет переданные поля книги. Если книга не найдена — генерируется доменная ошибка 404."
)
async def update_book(
    request: Request,
    book_id: Annotated[int, Form()],
    repo: BookRepoDeps,
    title: Annotated[str | None, Form()] = None,
    author: Annotated[str | None, Form()] = None,
    year: Annotated[int | None, Form()] = None,
):
    book_data = BookUpdate(title=title, author=author, year=year)
    await repo.update(book_id, book_data)
    
    books = await repo.list(skip=0, limit=10)
    return templates.TemplateResponse(
        request=request,
        name="books_list.html",
        context={"books": books}
    )

@router.delete(
    "/{book_id}",
    response_class=HTMLResponse,
    summary="Удалить книгу",
    description="Удаляет книгу из базы данных и возвращает обновленный список."
)
async def delete_book(
    request: Request,
    book_id: int,
    repo: BookRepoDeps
):
    await repo.delete(book_id)
    
    books = await repo.list(skip=0, limit=10)
    return templates.TemplateResponse(
        request=request,
        name="books_list.html",
        context={"books": books}
    )

""" Вспомогательные routes """

@router.get(
    "/api/get-book-info", 
    response_class=HTMLResponse,
    summary="Получить информацию о книге",
    description="Возвращает форму редактирования или информацию о книге по её id для htmx модалок."
)
async def get_book_info(
    request: Request,
    repo: BookRepoDeps,
    book_id: int
):
    # получение информации для htmx шаблона
    book = await repo.get(book_id)

    if book is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")
        
    return templates.TemplateResponse(
        request=request,
        name="book_info.html",
        context={"book": book}
    )