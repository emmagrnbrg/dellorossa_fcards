from sqlalchemy import Table, Column, Integer, String, ForeignKey

from backend.src.Database import BaseEntity

# избранные наборы пользователей
FavoriteSetEntity = Table(
    "favorite_sets",
    BaseEntity.metadata,
    Column("id", Integer, primary_key=True),
    Column("set_id", String, ForeignKey("sets.id")),
    Column("user_id", Integer, ForeignKey("users.id"))
)
