from typing import List, Optional, Dict, Any
from .database import db

async def get_books_by_author(author_name: str) -> List[Dict[str, Any]]:
    query = '''
    SELECT b.id, b.title, a.name AS author, c.name AS category, b.published_year, b.price
    FROM books b
    JOIN authors a ON b.author_id = a.id
    JOIN categories c ON b.category_id = c.id
    WHERE a.name = $1
    ORDER BY b.title ASC
    '''
    async with db.acquire() as conn:
        rows = await conn.fetch(query, author_name)
        return [dict(row) for row in rows]

async def get_books_by_category(category_name: str) -> List[Dict[str, Any]]:
    query = '''
    SELECT b.id, b.title, a.name AS author, c.name AS category, b.published_year, b.price
    FROM books b
    JOIN authors a ON b.author_id = a.id
    JOIN categories c ON b.category_id = c.id
    WHERE c.name = $1
    ORDER BY b.title ASC
    '''
    async with db.acquire() as conn:
        rows = await conn.fetch(query, category_name)
        return [dict(row) for row in rows]

# Utility for adding author and category efficiently (not blocking)
async def get_or_create_author(name: str) -> int:
    async with db.acquire() as conn:
        row = await conn.fetchrow('SELECT id FROM authors WHERE name=$1', name)
        if row:
            return row['id']
        row = await conn.fetchrow('INSERT INTO authors(name) VALUES($1) RETURNING id', name)
        return row['id']

async def get_or_create_category(name: str) -> int:
    async with db.acquire() as conn:
        row = await conn.fetchrow('SELECT id FROM categories WHERE name=$1', name)
        if row:
            return row['id']
        row = await conn.fetchrow('INSERT INTO categories(name) VALUES($1) RETURNING id', name)
        return row['id']

async def add_book(title: str, author: str, category: str, published_year: Optional[int], price: float) -> int:
    author_id = await get_or_create_author(author)
    category_id = await get_or_create_category(category)
    async with db.acquire() as conn:
        row = await conn.fetchrow(
            'INSERT INTO books(title, author_id, category_id, published_year, price) VALUES($1, $2, $3, $4, $5) RETURNING id',
            title, author_id, category_id, published_year, price
        )
        return row['id']

async def get_book_by_id(book_id: int) -> Optional[Dict[str, Any]]:
    query = '''
    SELECT b.id, b.title, a.name AS author, c.name AS category, b.published_year, b.price
    FROM books b
    JOIN authors a ON b.author_id = a.id
    JOIN categories c ON b.category_id = c.id
    WHERE b.id = $1
    '''
    async with db.acquire() as conn:
        row = await conn.fetchrow(query, book_id)
        if row:
            return dict(row)
        return None
