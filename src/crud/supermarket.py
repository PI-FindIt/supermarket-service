from src.crud.base import CrudBase
from src.filters import SupermarketFilter
from src.models import Supermarket


class CrudSupermarket(CrudBase[Supermarket, SupermarketFilter, int]):
    def __init__(self) -> None:
        super().__init__(Supermarket, SupermarketFilter)


crud_supermarket = CrudSupermarket()
