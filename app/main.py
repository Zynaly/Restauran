from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import menu, order
import time
from starlette.requests import Request

app = FastAPI(
    title="Restaurant API",
    description="API for managing restaurant menu and orders",
    version="1.0.0"
)

"""CORS middleware"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""Request logging middleware"""
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Request: {request.method} {request.url.path} - Completed in {process_time:.3f}s")
    return response

app.include_router(menu.router, prefix="/menu", tags=["Menu"])
app.include_router(order.router, prefix="/order", tags=["Order"])