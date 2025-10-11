from fastapi import FastAPI, Request, Depends, HTTPException, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path
from sqlalchemy.orm import Session
from decimal import Decimal
from pydantic import BaseModel
from typing import List

from src.db.database import get_session
from src.db.database_manager import DatabaseManager
from src.services.exchange_rate import ExchangeRate
from src.utils.data_loader import load_products_from_excel


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
#input schema
class ProductCreate(BaseModel):
    ProductID: str
    Name: str
    PriceUSD: Decimal

#output schema
class ProductRead(BaseModel):
    ProductID: str
    Name: str
    PriceUSD: Decimal
    
    class config:
        orm_mode=True
        
#----------products----------
@app.get("/api/products/", response_model=List[ProductRead])
def api_get_all_products():
    products= db_manager.get_all_products()
    return [{"ProductID": p.product_id, "Name": p.name, "PriceUSD": p.price} for p in products]


@app.get("/api/products/{product_id}", response_model=ProductRead)
def api_get_product_by_id(product_id: str):
    product = db_manager.get_product_by_id(product_id, None)
    if not product:
        raise HTTPException(status_code=404, detail="Product Not found")
    return ({"ProductID": product.product_id, "Name": product.name, "PriceUSD":product.price})

@app.get("/api/products/search/", response_model=List[ProductRead])
def api_get_products_by_name(name: str):
    products = db_manager.get_product_by_name(name)
    return [{"ProductID": p.product_id, "Name": p.name, "PriceUSD": p.price} for p in products]

@app.post("/api/products/", response_model=ProductRead)
def api_create_update_products(product: ProductCreate):
    result = db_manager.insert_single_product(product.dict())
    return {"ProductID": result["product_id"], "Name": product.Name, "PriceUSD": product.PriceUSD}

@app.delete("/api/products/{product_id}")
def api_delete_product(product_id: str):
    try:
        return db_manager.delete_product(product_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) 

@app.post("/aoi/products/upload/")
def api_upload_products(file: UploadFile = File(...)):
    #validata file type
    if not file.filename.endswith((".xls", ".xlsx")):
        raise HTTPException(status_code=400, detail= "Invalid file type. Must be EXCEL.")
       
    try:
        products_list = load_products_from_excel(file.file)
        results = db_manager.insert_or_update_products(products_list)
        return{"status": "success", "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process Excel file: {e}")
    
#----------Settings(ExchangeRate)----------
@app.get("/api/exchange-rate/")
def api_get_exchange_rate():
    ex = ExchangeRate()
    try:
        rate = ex.get_rate()
        return {"exchange_rate": rate}
    except ValueError:
        raise HTTPException(status_code=404, detail=" Exchange rate not set")

@app.post("/api/exchange-rate/")
def api_set_exchange_rate(rate: Decimal):
    ex = ExchangeRate()
    setting = ex.set_rate(rate)
    return{"Currency": setting.currency, "exchange_rate": setting.exchange_rate}

