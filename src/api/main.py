from pathlib import Path
from fastapi.templating import Jinja2Templates

#project and template path
PROJECT_ROOT=  Path(__file__).resolve().parents[2]
templates= Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))

