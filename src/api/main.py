from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path
from sqlalchemy.orm import Session
from decimal import Decimal
from pydantic import BaseModel

from src.db.database import get_session
from src.db.database_manager import DatabaseManager
from src.services.exchange_rate import ExchangeRate


#Create a DatabaseManager instance with local base_url
db_manager = DatabaseManager(qr_base_url="http://127.0.0.1:8000")

#templates path
BASE_DIR=Path(__file__).resolve().parent #C:\Users\Najla\Desktop\QR price updater\src\api
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

#fastapi application
app= FastAPI(title="Product QR Service")

#html page rout (QR code)
@app.get("/product/{product_id}", response_class=HTMLResponse)
def product_page(
    request: Request,
    product_id: str,
    session: Session = Depends(get_session),
    # session: Annotated[Session, Depends(get_session)]
):
    # unwrap generator if necessary
    if hasattr(session, "__next__"):
        session = next(session)

    #retrieving product
    product= db_manager.get_product_by_id(product_id= product_id, session=session)
    if not product:
        raise HTTPException(status_code=404, detail=" Product not found")
    
    
    ex_rate = ExchangeRate()  # pass the real session here
    try:
        local_price_str = f"{ex_rate.calculate_price(product.price)} تومان"
    except ValueError:
        local_price_str = "نرخ ارز تعریف نشده است"   
        
    #render HTML template
    product_dict = {
        "ProductID": product.product_id,
        "Name": product.name, 
        "PriceUSD": product.price
    }
    return templates.TemplateResponse(
        "product.html",
        {
            "request": request,
            "product": product_dict,
            "local_price": local_price_str,
        }
    )


#json API endpoints for progarm
#pydantic schemas
class ProductCreate(BaseModel):
    ProductID: str
    Name: str
    PriceUSD: Decimal
    
class ProductRead(BaseModel):
    ProductID: str
    Name: str
    PriceUSD: Decimal
    
    class config:
        orm_mode=True
