from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.users.routes import router as users_router
from app.auth.routes import router as auth_router


# Initialize FastAPI app with lifespan
app = FastAPI(title="FastAPI with JWT Auth", version="0.1.0")

app.add_middleware(GZipMiddleware, minimum_size=1000, compresslevel=5)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register auth routes
app.include_router(auth_router, prefix="/auth", tags=["Auth"])

# Register user routes
app.include_router(users_router, prefix="/users", tags=["Users"])

@app.exception_handler(StarletteHTTPException)
def http_exception_handler(_request, exc):
    """
    Custom exception handler for HTTPExceptions
    """
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

@app.exception_handler(RequestValidationError)
def validation_exception_handler(_request, exc):
    """
    Custom exception handler for RequestValidationErrors
    """
    return JSONResponse(status_code=400, content={"detail": exc.errors()})
