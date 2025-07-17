from aiogoogle import Aiogoogle

from app.core.config import settings


async def spreadsheets_create(wrapper_service: Aiogoogle) -> str:
    """
    Создание документа.
    """
    service = await wrapper_service.discover("sheets", "v4")
    body = {
        "properties": {"title": "Информация по проектам", "locale": "ru_RU"},
        "sheets": [
            {
                "properties": {
                    "sheetType": "GRID",
                    "sheetId": 0,
                    "title": "Лист1",
                    "gridPorerties": {"rowCount": 50, "columnCount": 3},
                }
            }
        ],
    }

    response = service.spreadsheets.create(json=body)
    spreadsheet_id = response["spreadsheetId"]
    return spreadsheet_id


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_service: Aiogoogle) -> None:
    """
    Выдача прав доступа.
    """
    permissions_body = {
        "type": "user",
        "role": "writer",
        "emailAddress": settings.email,
    }
    service = await wrapper_service.discover("drive", " v3")
    await wrapper_service.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id, json=permissions_body, fields="id"
        )
    )


async def spreadsheets_update_value(
    spreadsheet_id: str, wrapper_service: Aiogoogle, projects: list
) -> None:
    """
    Заполнение документа.
    """

    service = await wrapper_service.discover("sheets", "v4")
    table_body = [
        ["Отчет от", ""],
        ["Топ проектов по скорости закрытия"],
        ["Название проекта", "Время сбора", "Описание"],
    ]

    for project in projects:
        new_row = [
            str(project.name),
            str(project.close_date - project.create_date),
            str(project.description),
        ]
        table_body.append(new_row)

    update_body = {"majorDimension": "ROWS", "values": table_body}
    await wrapper_service.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range="A1:C30",
            valueInputOption="USER_ENTERED",
            json=update_body,
        )
    )
