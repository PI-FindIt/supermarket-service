INSERT INTO supermarket(name, logo, image, services, description)
VALUES ('Pingo Doce',
        'pingo-doce/logo.png',
        'pingo-doce/image.png',
        ARRAY ['COFFEE', 'GAS_STATION', 'NEWSSTAND', 'PHARMACY', 'RESTAURANT', 'SELF_KIOSK']::supermarketservices[],
        'Pingo Doce is a supermarket chain in Portugal, known for its wide range of products and competitive prices. It offers a variety of services including coffee shops, gas stations, and self-service kiosks.');

INSERT INTO supermarket(name, logo, image, services, description)
VALUES ('Mercadona',
        'mercadona/logo.svg',
        'mercadona/image.png',
        ARRAY ['COFFEE', 'RESTAURANT']::supermarketservices[],
        'Mercadona is a Spanish supermarket chain that has expanded into Portugal. It is known for its high-quality products, low prices and commitment to customer satisfaction. In Portugal, Mercadona offers a variety of services including coffee shops and restaurants.');

INSERT INTO supermarket(name, logo, image, services, description)
VALUES ('Continente',
        'continente/logo.svg',
        'continente/image.jpg',
        ARRAY ['COFFEE', 'GAS_STATION', 'PHARMACY', 'RESTAURANT', 'SELF_KIOSK']::supermarketservices[],
        'Continente is one of the largest supermarket chains in Portugal, offering a diverse selection of products and services. It is known for its loyalty program and commitment to sustainability.');

INSERT INTO supermarket(name, logo, image, services, description)
VALUES ('Lidl',
        'lidl/logo.svg',
        'lidl/image.png',
        ARRAY []::supermarketservices[],
        'Lidl is a global discount supermarket chain, known for its low prices and high-quality products. In Portugal, Lidl offers a variety of services including Parkside machines and lifestyle products.');

INSERT INTO supermarket(name, logo, image, services, description)
VALUES ('Aldi',
        'aldi/logo.svg',
        'aldi/image.jpg',
        ARRAY []::supermarketservices[],
        'Aldi is a global discount supermarket chain, known for its low prices and high-quality products. In Portugal, Aldi Nord operates the brand.');

INSERT INTO supermarket(name, logo, image, services, description)
VALUES ('Auchan',
        'auchan/logo.svg',
        'auchan/image.png',
        ARRAY ['COFFEE', 'GAS_STATION', 'NEWSSTAND', 'PHARMACY', 'SELF_KIOSK']::supermarketservices[],
        'Auchan is a multinational retail group, operating hypermarkets and supermarkets in Portugal. It offers a wide range of products and services, including bio products and self service spices.');

INSERT INTO supermarket(name, logo, image, services, description)
VALUES ('Intermarché',
        'intermarche/logo.svg',
        'intermarche/image.jpg',
        ARRAY ['COFFEE', 'GAS_STATION', 'NEWSSTAND', 'RESTAURANT']::supermarketservices[],
        'Intermarché is a popular supermarket chain in Portugal, part of the Les Mousquetaires group. It offers a variety of products and services, as well as CMTV interviews: Murtosa has a famous Intermarché because of Mónica, the missing pregnant woman.');

INSERT INTO supermarket(name, logo, image, services, description)
VALUES ('Minipreço',
        'minipreco/logo.svg',
        'minipreco/image.png',
        ARRAY ['COFFEE']::supermarketservices[],
        'Minipreço is a supermarket chain in Portugal, known for its high prices and bad range of products. Thank you Auchan for buying it and getting rid of it in the next months.');
