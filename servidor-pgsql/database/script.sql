-- Crear una tablas

CREATE TABLE
    users (
        id SERIAL PRIMARY KEY NOT NULL,
        username VARCHAR(100) NOT NULL,
        password VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL
    )