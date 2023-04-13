from fastapi import APIRouter

from app.handler import test, demo


def register_router(app):
    v1_router = APIRouter()
    v1_router.include_router(test.ROUTER, prefix='/test')

    v2_router = APIRouter()
    v2_router.include_router(demo.ROUTER, prefix='/demo')

    app.include_router(v1_router, prefix='/api/v1')
    app.include_router(v2_router, prefix='/api/v2')
