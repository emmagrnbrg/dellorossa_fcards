from sqlalchemy import Table, Column, Integer, String, ForeignKey

from backend.src.Database import BaseEntity

# пользователи с доступом к набору с типом доступа USER_RESTRICTED
SetMemberEntity = Table(
    "set_members",
    BaseEntity.metadata,
    Column("id", Integer, primary_key=True),
    Column("set_id", String, ForeignKey("sets.id")),
    Column("member_id", Integer, ForeignKey("users.id"))
)
