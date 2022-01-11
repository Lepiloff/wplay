import math
import asyncio

import folium
import geocoder

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from db import database
from helpers.middleware import add_user_data_to_request
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
app.middleware('http')(add_user_data_to_request)

# Custom endpoints
app.include_router(api_router)







#TODO чекнуть может ли одна локация быть у разных ивентов (если это например спортцентр)
#TODO почекать на удаление связанных таблиц (ONDELATE = ....)
# TODO судя по этому https://fastapi.tiangolo.com/advanced/templates/  надо везде в использовать response_class=HTMLResponse
# TODO использовать UUIDField  в качестве адишников  в моделях
# TODO добавить индексы в БД
# TODO безопасность чекнуть, формы и прочее
#TODO в роутах вызов логики везде через try/except


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
@app.get("/get_location", response_class=HTMLResponse)
async def read_item(request: Request):
    #print(request.body())
    #return templates.TemplateResponse("index.html", {"request": request})
    city = geocoder.ip('me').city
    g = geocoder.osm(f'дзержинского 11, {city}')
    #print(g.json)
    current_coord = g.latlng
    print(g.latlng)
    print(city)
    print(distance(current_coord, (53.8915, 27.5279)))
    start_coords = (46.9540700, 142.7360300)
    folium_map = folium.Map(location=current_coord, zoom_start=19)
    c= folium.LatLngPopup()
    folium_map.add_child(c)
    return folium_map._repr_html_()


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

@app.route("/get_coord", methods=['GET', 'POST'])
def read_root(request: Request):
    print (request)
    start_coords = (46.9540700, 142.7360300)
    folium_map = folium.Map(location=start_coords, zoom_start=14)
    c= folium.LatLngPopup()
    folium_map.add_child(c)
    folium_map.save("templates/map.html")
    return templates.TemplateResponse("index.html", {"request": request})
##################################

# TODO транзакции где надо (при множественном добавлениии\изменении существенно ускоряют запись в БД)