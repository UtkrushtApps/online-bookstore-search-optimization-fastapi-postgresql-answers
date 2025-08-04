# Solution Steps

1. Review the current database schema and identify columns frequently used in search filters: author and category.

2. Refactor the schema to normalize authors and categories into separate tables (authors, categories) and store foreign keys in the books table.

3. Add appropriate indexes to books.author_id and books.category_id to enable fast searches on these fields.

4. Ensure that the ORM or DB access layer uses async and non-blocking methods (asyncpg, connection pooling).

5. Rewrite the query logic in the database access layer (e.g., in crud.py) to join books with authors and categories using efficient async SQL and to use parameterized queries.

6. Implement utility functions to look up (or create) author and category entries during book insertion in an efficient async way.

7. Use only asyncpg and async methods for all database queries and inserts, avoiding blocking DB access in request handlers.

8. Refactor the database module to expose a singleton database pool, and expose async acquire context for DB connections.

9. (Optionally) Add title index if partial title search or ordering is frequent.

10. Provide an initialization script to connect and disconnect the database pool automatically on FastAPI startup/shutdown.

