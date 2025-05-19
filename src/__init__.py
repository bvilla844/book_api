from fastapi import FastAPI
from src.books.routes import book_router
from src.auth.routes import auth_router
from src.reviews.routes import review_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from .errors import register_all_errors
from .middleware import register_middleware
import os
from pathlib import Path

@asynccontextmanager
async def life_span(app: FastAPI):
    print(f"server is starting..")
    await init_db()
    yield
    print(f"server has been stopped..")
    print("🧭 Diagnostic info (Render environment)")
    print("📂 Current working directory:", os.getcwd())
    print("📄 __file__:", __file__)
    print("📂 BASE_DIR:", Path(__file__).resolve().parent)
    print("📂 TEMPLATE_FOLDER:", Path(__file__).resolve().parent / "templates")
    print("📁 TEMPLATE_FOLDER exists:", (Path(__file__).resolve().parent / "templates").exists())

version = "v1"

app = FastAPI(
    title="Bookly",
    description="AREST API for a book review wev service",
    version=version,
    lifespan=life_span,
)

register_all_errors(app)
register_middleware(app)



app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["auth"])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=["reviews"])


