import dataclasses
import json
from dataclasses import dataclass
from typing import Any

import osmium
from osmium.osm.types import Node, Way
from unidecode import unidecode

id_mapping = {
    "pingo": 1,
    "mercadona": 2,
    "continente": 3,
    "lidl": 4,
    "aldi": 5,
    "auchan": 6,
    "intermarche": 7,
    "minipreco": 8,
}


@dataclass
class Supermarket:
    id: int
    lat: float
    lon: float
    name: str | None = None

    def to_sql(self) -> str:
        name = f"'self.name'" if self.name else "NULL"
        return f"INSERT INTO supermarket_location (supermarket_id, id, name, latitude, longitude) VALUES ({self.id}, DEFAULT, {name}, {self.lat}, {self.lon});"


supermarkets: list[Supermarket] = []


def get_supermarket_id(brand: str) -> int:
    brand = unidecode(brand.lower())
    for name, id in id_mapping.items():
        if name in brand:
            return id
    return -1


class NamesHandler(osmium.SimpleHandler):
    def __init__(self) -> None:
        super().__init__()
        self.node_locations: dict[str, tuple[float, float]] = {}

    def node(self, n: Node) -> None:
        self.node_locations[n.id] = (n.location.lat, n.location.lon)
        if "shop" not in n.tags:
            return

        if n.tags["shop"] != "supermarket":
            return

        if "brand" not in n.tags:
            return

        lat, lon = n.location.lat, n.location.lon
        supermarket_id = get_supermarket_id(n.tags["brand"])

        if supermarket_id == -1:
            return
        supermarkets.append(
            Supermarket(
                id=supermarket_id,
                lat=lat,
                lon=lon,
                name=n.tags.get("branch"),
            )
        )

    def way(self, w: Way) -> None:
        if "shop" not in w.tags:
            return

        if w.tags["shop"] != "supermarket":
            return

        if "brand" not in w.tags:
            return

        if (supermarket_id := get_supermarket_id(w.tags["brand"])) == -1:
            return

        if not w.nodes:
            return

        coords = []
        for node_ref in w.nodes:
            node_id = node_ref.ref
            if node_id in self.node_locations:
                coords.append(self.node_locations[node_id])

        if not coords:
            return

        avg_lat = sum(lat for lat, lon in coords) / len(coords)
        avg_lon = sum(lon for lat, lon in coords) / len(coords)
        supermarkets.append(
            Supermarket(
                id=supermarket_id,
                lat=avg_lat,
                lon=avg_lon,
                name=w.tags.get("branch"),
            )
        )


print("Parsing OSM file. This may take a while.")
NamesHandler().apply_file("portugal.osm.pbf")


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


print(len(supermarkets), "supermarkets found")

with open("supermarkets.json", "w") as f:
    print("Writing supermarkets.json")
    f.write(
        json.dumps(supermarkets, indent=2, cls=EnhancedJSONEncoder, ensure_ascii=False)
    )

with open("../migrations/locations.sql", "w") as f:
    print("Writing supermarkets.sql")
    for supermarket in supermarkets:
        f.write(supermarket.to_sql() + "\n")
