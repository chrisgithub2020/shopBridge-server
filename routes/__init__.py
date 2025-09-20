from .auth import router as auth_router
from .consumer import router as consumer_router
from .seller import router as seller_router

__all__ = ["auth_router", "consumer_router", "seller_router"]