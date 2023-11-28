"""
Main
"""
import src.models as models

from fastapi import FastAPI, Request, Depends, Form, Path, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from src.database import init_db, get_db
from loguru import logger

app = FastAPI()
templates = Jinja2Templates(directory='web/html')

init_db()
app.mount('/web', StaticFiles(directory='web'), name='web')
logger = logger.opt(colors=True)


@app.get('/')
async def home(request: Request,
               database: Session = Depends(get_db)) -> templates.TemplateResponse:
	"""
	Main page
    """
	logger.info('Opening home page')
	task = database.query(models.Task).order_by(models.Task.id.desc())

	return templates.TemplateResponse('index.html', {'request': request, 'tasks': task})


@app.get('/list')
async def list(request: Request,
               database: Session = Depends(get_db)) -> templates.TemplateResponse:
	"""
	List page
    """
	logger.info('Opening list page')
	task = database.query(models.Task).order_by(models.Task.id.desc())

	return templates.TemplateResponse('list.html', {'request': request, 'tasks': task})


@app.post('/add')
async def add(task: str = Form(default='', max_length=500),
              database: Session = Depends(get_db)) -> RedirectResponse:
	"""
	Add new task
	"""
	task = models.Task(text=task)

	logger.info(f'Creating task: {task.text}')
	database.add(task)
	database.commit()

	return RedirectResponse(url=app.url_path_for('home'),
	                        status_code=status.HTTP_303_SEE_OTHER)


@app.get('/edit/{task_id}')
async def edit_get(request: Request,
                   database: Session = Depends(get_db),
                   task_id: int = Path(gt=0)) -> RedirectResponse:
	"""
	Edit existed task
	"""
	task = database.query(models.Task).filter(models.Task.id == task_id).first()

	logger.info(f'Editing task: {task}.')

	return templates.TemplateResponse("edit.html",
	                                  {"request": request, "task": task})
