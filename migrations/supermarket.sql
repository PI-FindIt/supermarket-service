INSERT INTO supermarket(name, image, services, description)
VALUES ('Pingo Doce',
        'logos/pingo-doce.svg',
        ARRAY ['COFFEE', 'GAS_STATION', 'NEWSSTAND', 'PHARMACY', 'RESTAURANT', 'SELF_KIOSK']::supermarketservices[],
        'Pingo Doce is a supermarket chain in Portugal, known for its wide range of products and competitive prices. It offers a variety of services including coffee shops, gas stations, and self-service kiosks.');

INSERT INTO supermarket(name, image, services, description)
VALUES ('Mercadona',
        'logos/mercadona.svg',
        ARRAY ['COFFEE', 'RESTAURANT']::supermarketservices[],
        'Mercadona is a Spanish supermarket chain that has expanded into Portugal. It is known for its high-quality products, low prices and commitment to customer satisfaction. In Portugal, Mercadona offers a variety of services including coffee shops and restaurants.');

INSERT INTO supermarket(name, image, services, description)
VALUES ('Continente',
        'logos/continente.svg',
        ARRAY ['COFFEE', 'GAS_STATION', 'PHARMACY', 'RESTAURANT', 'SELF_KIOSK']::supermarketservices[],
        'Continente is one of the largest supermarket chains in Portugal, offering a diverse selection of products and services. It is known for its loyalty program and commitment to sustainability.');

INSERT INTO supermarket(name, image, services, description)
VALUES ('Lidl',
        'logos/lidl.svg',
        ARRAY []::supermarketservices[],
        'Lidl is a global discount supermarket chain, known for its low prices and high-quality products. In Portugal, Lidl offers a variety of services including coffee shops and gas stations.');

INSERT INTO supermarket(name, image, services, description)
VALUES ('Aldi',
        'logos/aldi.svg',
        ARRAY []::supermarketservices[],
        'Aldi is a global discount supermarket chain, known for its low prices and high-quality products. In Portugal, Aldi offers a variety of services including coffee shops and gas stations.');

INSERT INTO supermarket(name, image, services, description)
VALUES ('Auchan',
        'logos/auchan.svg',
        ARRAY ['COFFEE', 'GAS_STATION', 'NEWSSTAND', 'PHARMACY', 'SELF_KIOSK']::supermarketservices[],
        'Auchan is a multinational retail group, operating hypermarkets and supermarkets in Portugal. It offers a wide range of products and services, including gas stations and restaurants.');

INSERT INTO supermarket(name, image, services, description)
VALUES ('Intermarché',
        'logos/intermarche.svg',
        ARRAY ['COFFEE', 'GAS_STATION', 'NEWSSTAND', 'RESTAURANT']::supermarketservices[],
        'Intermarché is a popular supermarket chain in Portugal, part of the Les Mousquetaires group. It offers a variety of products and services, including gas stations and restaurants.');

INSERT INTO supermarket(name, image, services, description)
VALUES ('Minipreço',
        'logos/minipreco.svg',
        ARRAY ['COFFEE']::supermarketservices[],
        'Minipreço is a discount supermarket chain in Portugal, known for its low prices and wide range of products. It focuses on providing value to customers with a no-frills shopping experience.');
