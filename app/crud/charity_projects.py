from app.models.charity_project import CharityProject

from .base import BaseCRUD


class ProjectCRUD(BaseCRUD):
    """Класс для объекта проектов. Для создания CRUD."""


project = ProjectCRUD(CharityProject)
