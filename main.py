import math

import folium
import geocoder

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from models.users import users

from db import database
from routes import api_router

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


# Custom endpoints
app.include_router(api_router)


@app.post("/simple_users")
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