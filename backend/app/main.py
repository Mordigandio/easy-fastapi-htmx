from app.routes.book import router as book_route
from app.utils.templates import templates
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="library",
    version="0.1.0"
)

app.include_router(book_route)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", )

@app.get("/api/get-modal")
async def get_modal(request: Request, type: str = "list"):
    return templates.TemplateResponse(request=request, name="modal.html", context={"modal_type": type})