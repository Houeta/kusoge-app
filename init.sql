
CREATE TABLE auth_user (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    email VARCHAR (255) NOT NULL,
    name VARCHAR (255) NOT NULL,
    password VARCHAR (255) NOT NULL
);

INSERT INTO auth_user (email, name, password) VALUES ('iambatmanthegoat@gmail.com', miracle, '123456');

# Create table for catalog service

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    description TEXT,
    price NUMERIC NOT NULL
);