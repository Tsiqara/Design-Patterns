import os
import sqlite3

from fastapi import FastAPI

from pos.infra.fastapi import unit_api
from pos.infra.fastapi.products import product_api
from pos.infra.fastapi.receipts import receipt_api
from pos.infra.fastapi.sales import sales_api
from pos.infra.sqlite.products_repo import SQLProductRepository
from pos.infra.sqlite.receipts_repo import SQLReceiptRepository
from pos.infra.sqlite.units_repo import SQLUnitRepository


def get_db_file() -> str:
    file = os.path.abspath("pos.db")
    file = os.path.dirname(file)
    file = os.path.dirname(file)
    return os.path.join(file, "infra", "sqlite", "pos.db")


def init_app() -> FastAPI:
    app = FastAPI()
    app.include_router(unit_api)
    app.include_router(product_api)
    app.include_router(receipt_api)
    app.include_router(sales_api)
    con = sqlite3.Connection(get_db_file(), check_same_thread=False)
    cur = con.cursor()
    app.state.units = SQLUnitRepository(con, cur)
    app.state.products = SQLProductRepository(con, cur)
    app.state.receipts = SQLReceiptRepository(con, cur)
    return app
