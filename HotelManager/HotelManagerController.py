from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, Form
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from HotelManager.application.Language import Language
from HotelManager.application.model.HotelRoomDTO import HotelRoomDTO, HotelRoomTypeMapper
from HotelManager.application.model.WebHotelRoomOverviewDTO import WebHotelRoomOverviewDTO
from HotelManager.application.services.HotelManagerService import HotelManagerService

app = FastAPI()

path = Path(__file__)
root_directory = path.parent

templates = Jinja2Templates(directory=root_directory.joinpath('web/templates'))
app.mount('/static', StaticFiles(directory=root_directory.joinpath('web/static')), name='static')

hotel_manager_service = HotelManagerService(root_directory.parent)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    hotelroom_overview_dto = WebHotelRoomOverviewDTO(
        list_of_rooms=hotel_manager_service.get_all_hotelrooms(Language.GERMAN)
    )

    return templates.TemplateResponse('index.html',
                                      {'request': request, 'hotelroom_overview_dto': hotelroom_overview_dto})


@app.post("/update_hotelroom/{old_room_id}")
async def update_hotelroom(request: Request,
                           old_room_id: int,
                           room_id: Annotated[int, Form()],
                           room_size: Annotated[str, Form()],
                           has_minibar: Annotated[str, Form()] = None):
    hotelroom = HotelRoomDTO(room_id=room_id,
                             room_size=HotelRoomTypeMapper().string_to_type(room_size),
                             has_minibar=(has_minibar == 'True'))

    hotel_manager_service.update_room(old_room_id, hotelroom)

    hotelroom_overview_dto = WebHotelRoomOverviewDTO(
        list_of_rooms=hotel_manager_service.get_all_hotelrooms(Language.GERMAN)
    )

    return templates.TemplateResponse('/html_fragments/hotelroom_overview_table.html',
                                      {'request': request, 'hotelroom_overview_dto': hotelroom_overview_dto})


@app.put("/add_new_hotelroom")
async def add_new_hotelroom(request: Request,
                            room_id: Annotated[int, Form()],
                            room_size: Annotated[str, Form()],
                            has_minibar: Annotated[str, Form()] = None):
    hotelroom = HotelRoomDTO(room_id=room_id,
                             room_size=HotelRoomTypeMapper().string_to_type(room_size),
                             has_minibar=(has_minibar == 'True'))

    hotel_manager_service.add_hotelroom(hotelroom)

    hotelroom_overview_dto = WebHotelRoomOverviewDTO(
        list_of_rooms=hotel_manager_service.get_all_hotelrooms(Language.GERMAN)
    )

    return templates.TemplateResponse('/html_fragments/hotelroom_overview_table.html',
                                      {'request': request, 'hotelroom_overview_dto': hotelroom_overview_dto})


@app.delete("/delete_hotelroom/{room_id}")
async def delete_hotelroom(request: Request, room_id: int):
    hotel_manager_service.delete_hotelroom(room_id)

    return {}

@app.get("/get_add_new_hotelroom_form")
async def get_new_hotelroom_form(request: Request):
    return templates.TemplateResponse('/html_fragments/add_new_hotelroom.html', {'request': request})


@app.get("/cancel_add_new_hotelroom")
async def cancel_add_new_hotelroom(request: Request):
    return templates.TemplateResponse('/html_fragments/base_add_new_hotelroom_row.html', {'request': request})


@app.get("/update_form/{room_id}", response_class=HTMLResponse)
async def get_update_hotelroom_form(request: Request, room_id: int):
    hotelroom_web = hotel_manager_service.get_information_hotelroom(room_id)

    return templates.TemplateResponse('/html_fragments/update_hotelroom_form.html',
                                      {'request': request, 'hotelroom_row': hotelroom_web})

@app.get("/cancel_edit_hotelroom/{room_id}")
async def cancel_edit_hotelroom(request: Request, room_id: int):
    hotelroom_web = hotel_manager_service.get_information_hotelroom(room_id, Language.GERMAN)

    return templates.TemplateResponse('/html_fragments/base_hotelroom_row.html',
                                      {'request': request, 'hotelroom_row': hotelroom_web})
