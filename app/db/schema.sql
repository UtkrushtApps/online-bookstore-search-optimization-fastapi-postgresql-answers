-- Optimized schema for online bookstore
CREATE TABLE IF NOT EXISTS authors (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    author_id INTEGER NOT NULL REFERENCES authors(id),
    category_id INTEGER NOT NULL REFERENCES categories(id),
    published_year INTEGER,
    price NUMERIC(10,2)
);

-- Add indexes to optimize search operations
CREATE INDEX IF NOT EXISTS idx_books_author_id ON books(author_id);
CREATE INDEX IF NOT EXISTS idx_books_category_id ON books(category_id);

-- Optionally, cover for frequent title searches as well
CREATE INDEX IF NOT EXISTS idx_books_title ON books(title);