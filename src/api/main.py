from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path
from sqlalchemy.orm import Session
from decimal import Decimal
from typing import Annotated, Any
from src.db.database import get_session

from src.db.database_manager import DatabaseManager
from src.services.exchange_rate import ExchangeRate

#Create a DatabaseManager instance with local base_url
db = DatabaseManager(qr_base_url="http://127.0.0.1:8000")

#templates path
BASE_DIR=Path(__file__).resolve().parent #C:\Users\Najla\Desktop\QR price updater\src\api
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

#fastapi application
app= FastAPI(title="Product QR Service")

@app.get("/product/{product_id}", response_class=HTMLResponse)
def product_page(
    request: Request,
    product_id: str,
    # session: Session = Depends(get_session),
    session: Annotated[Session, Depends(get_session)]
):
    #retrieving product
    product= db.get_product_by_id(product_id= product_id, session=session)
    if not product:
        raise HTTPException(status_code=404, detail=" Product not found")
    
    #price calculating
    ex_rate= ExchangeRate(session=session)
    if ex_rate.get_rate() == Decimal(-1):
        local_price_str= "نرخ ارز تعریف نشده است"
    else:
        local_price=ex_rate.calculate_price(product.price)
        local_price_str= f"{local_price} تومان"
        
    #render HTML template
    
    product_dict = {
        "ProductID": product.ProductID,
        "Name": product.Name, 
        "PriceUSD": product.PriceUSD
    }
    return templates.TemplateResponse(
        "product.html",
        {
            "request": request,
            "product": product_dict,
            "local_price": local_price_str,
        }
    )
