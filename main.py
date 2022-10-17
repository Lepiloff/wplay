import math

from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from db import database
from helpers.middleware import get_user_notifications, set_custom_attr
from models.users import users
from routes import api_router
from sessions.core.base import redis_cache

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
# TODO add status_code


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.on_event('startup')
async def starup_event():
    await redis_cache.init_cache()


@app.on_event('shutdown')
async def shutdown_event():
    await redis_cache.close()


# Custom middleware
app.middleware('http')(get_user_notifications)
app.middleware('http')(set_custom_attr)

# Custom endpoints
app.include_router(api_router)






#TODO в модели user поле is_notified сделать index=True
#TODO чекнуть может ли одна локация быть у разных ивентов (если это например спортцентр)
#TODO почекать на удаление связанных таблиц (ONDELATE = ....)
# TODO судя по этому https://fastapi.tiangolo.com/advanced/templates/  надо везде в использовать response_class=HTMLResponse
# TODO использовать UUIDField  в качестве адишников  в моделях
# TODO добавить индексы в БД
# TODO безопасность чекнуть, формы и прочее
#TODO в роутах вызов логики везде через try/except
# TODO транзакции где надо (при множественном добавлениии\изменении существенно ускоряют запись в БД)
#TODO то что по критериям не отображается в шаблоне, типа кнопка на добавление в ивент, надо проверять и в логике критерии.  Т.е дублировать проверку и в шаблоне и во вьюхе


@app.post("/simple_users")
# TODO тут за стиль переносов с тобой надо побазарить
async def _users(request: Request, name: str = Form(...)):
    email, phone, surname, age, personal_info, hashed_password = \
        'email', 'phone', 'surname', 'age', 'personal_info', 'hashed_password'
    query = "INSERT INTO users(email, phone, name, surname, age, personal_info, hashed_password) " \
            "VALUES (:email, :phone, :name, :surname, :age, :personal_info, :hashed_password) "
    values = {"email": email, "phone": phone, "name": name, "surname": surname,
              "age": age, "personal_info": personal_info, "hashed_password": hashed_password}
    result = await database.execute(query=query, values=values)
    result = dict(result)
    return templates.TemplateResponse('users.html', context={'request': request, 'result': result})


@app.get("/simple_users")
async def _users(request: Request):
    query = users.select()
    result = await database.fetch_all(query=query)
    result = [dict(r) for r in result]
    return templates.TemplateResponse('users.html', context={'request': request, 'result': result})


##############


def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d

##################################