from aiogram import Router

from devspace_bot.handlers.contacts import router as contacts_router
from devspace_bot.handlers.estimate import router as estimate_router
from devspace_bot.handlers.portfolio import router as portfolio_router
from devspace_bot.handlers.start import router as start_router


def build_router() -> Router:
    router = Router()
    router.include_router(start_router)
    router.include_router(estimate_router)
    router.include_router(portfolio_router)
    router.include_router(contacts_router)
    return router

