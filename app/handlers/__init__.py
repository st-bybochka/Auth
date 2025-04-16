from app.handlers.user_handler import router as user_router
from app.handlers.auth_handler import router as auth_router
from app.handlers.task_handler import router as task_router


routers = [user_router, auth_router, task_router]