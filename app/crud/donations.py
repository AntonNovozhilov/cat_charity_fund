from app.models.donation import Donation

from .base import BaseCRUD


class DonationCRUD(BaseCRUD):
    """Класс для объекта донатов. Для создания CRUD."""

    pass


donation = DonationCRUD(Donation)
