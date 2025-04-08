from src.crud.base import CrudBase
from src.models import Supermarket


class CrudSupermarket(CrudBase[Supermarket, None, int]):
    def __init__(self) -> None:
        super().__init__(Supermarket, None)


crud_supermarket = CrudSupermarket()
