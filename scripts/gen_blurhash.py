from io import BytesIO

import blurhash
import cairosvg
import requests
from PIL import Image

supermarkets: dict[str, tuple[str, str]] = {
    "pingo-doce": ("logo.png", "image.jpg"),
    "mercadona": ("logo.svg", "image.jpg"),
    "continente": ("logo.svg", "image.jpg"),
    "lidl": ("logo.svg", "image.jpg"),
    "aldi": ("logo.svg", "image.jpg"),
    "auchan": ("logo.svg", "image.png"),
    "intermarche": ("logo.svg", "image.jpg"),
    "minipreco": ("logo.svg", "image.jpg"),
}

for supermarket, images in supermarkets.items():
    for image_url in images:
        url = f"http://localhost/cdn/supermarket/{supermarket}/{image_url}"
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Error fetching image {url}: {response.status_code}")
            continue

        if image_url.endswith(".svg"):
            out = BytesIO()
            cairosvg.svg2png(response.content, write_to=out)
        else:
            out = BytesIO(response.content)

        with Image.open(out) as image:
            image.thumbnail((100, 100))
            hash = blurhash.encode(image, x_components=3, y_components=3)
            print(f"Blurhash for {supermarket} {image_url}: {hash.replace(':', '\\:')}")
