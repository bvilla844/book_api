from fastapi import FastAPI
from fastapi.requests import Request
import time
import logging
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

logger = logging.getLogger('uvicorn.access') 
logger.disabled = True

def register_middleware(app:FastAPI):
    
    @app.middleware('http')
    async def custom_loggin(request: Request, call_next):
        start_time = time.time()
        print("before", start_time)

        response = await call_next(request)
        processing_time = time.time() - start_time

        message = f"{request.method} - {request.url.path} - {response.status_code} - completed afte {processing_time}s "
        print(message)
        return response
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins = ["*"],
        allow_headers = ["*"],
        allow_methods = ["*"],
        allow_credentials = True
    )
    
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["localhost", "127.0.0.1","book-api-gvu9.onrender.com"]
    )