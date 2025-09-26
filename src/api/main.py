from pathlib import Path
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, Depends, HTTPException
from src.db.database_manager import DatabaseManager
from src.services.exchange_rate import ExchangeRate
from decimal import Decimal
#project and template path
PROJECT_ROOT=  Path(__file__).resolve().parents[2]
templates= Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))

app = FastAPI()

db= DatabaseManager(f"sqlite:///{PROJECT_ROOT}/data/app.db")

#dependency for Session
def get_session():
    #create a session and automatically release it after work is done
    with db.Session() as session:
        yield session


#endpoints
@app.get(f"/product/{"product_id"}")
async def product_page(request: Request, product_id: str, session=Depends(get_session)):
    #Exchange instance
    exchange = ExchangeRate(session) 
    
    #retrieve product from DB
    product= db.get_product_by_id(product_id)   
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    #calculate local price
    original_price= Decimal(str(product.price))
    local_price= exchange.calculate_price(original_price,)