import pytest
from fastapi.testclient import TestClient
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.api.main import app
from src.services.qrcode_generator import QRCodeGenerator
from src.db.database import init_db
from src.db.database_manager import DatabaseManager
#----------Test Client----------
client= TestClient(app)

#test Qr codes png files
BASE_DIR= os.path.dirname(os.path.abspath(__file__)) #c:\Users\Najla\Desktop\QR price updater\tests
QR_TEST_DIR = os.path.join(BASE_DIR, "tets_qrcodes")
os.makedirs(QR_TEST_DIR, exist_ok=True)
qr_gen= QRCodeGenerator("http://127.0.0.1:8000", png_files_dir=QR_TEST_DIR)

#----------fixtures----------
@pytest.fixture
def temp_session():
    """temp in-memory database for each test"""
    engine= create_engine("sqlite:///:memory:", future=True)
    init_db(engine_arg=engine)
    SessionLocal=sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    session= SessionLocal()
    yield session
    session.close()
    engine.dispose()
    
    
@pytest.fixture
def db_manager():
    """database manager without default session"""
    return DatabaseManager(qr_base_url="http://127.0.0.1:8000")

