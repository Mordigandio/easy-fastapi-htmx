from app.domain.exception import DomainError
from app.routes.book import router as book_route
from app.utils.templates import templates
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="library",
    version="0.1.0"
)

@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="error.html",
        context={"message": exc.message}, 
        status_code=exc.status_code        
    )

app.include_router(book_route)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    # главная страница приложения
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/api/get-modal")
async def get_modal(request: Request, type: str = "list"):
    # получение модального окна по типу
    return templates.TemplateResponse(
        request=request, 
        name="modal.html", 
        context={"modal_type": type}
    )