from sqlalchemy import Column, Integer, Table, ForeignKey

from backend.src.Database import BaseEntity

RoleRightEntity = Table(
    "roles_rights",
    BaseEntity.metadata,
    Column("id", Integer, primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id")),
    Column("right_id", Integer, ForeignKey("rights.id"))
)  # связка ролей и прав в системе
