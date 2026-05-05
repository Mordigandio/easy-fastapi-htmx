from app.routes.book import router as book_route
from fastapi import FastAPI

app = FastAPI(
    title="library",
    version="0.1.0"
)

app.include_router(book_route)

@app.get("/")
async def health_check():
    return {"status": "ok", "service": "Book Service"}