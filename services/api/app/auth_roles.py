from __future__ import annotations

from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    OWNER = "owner"
    DEVELOPER = "developer"
    ANALYST = "analyst"
    VIEWER = "viewer"


ROLE_HIERARCHY = {
    UserRole.ADMIN: 5,
    UserRole.OWNER: 4,
    UserRole.DEVELOPER: 3,
    UserRole.ANALYST: 2,
    UserRole.VIEWER: 1,
}


def role_can_access(required_role: UserRole | str, user_role: UserRole | str) -> bool:
    required_value = ROLE_HIERARCHY.get(UserRole(required_role), 0)
    user_value = ROLE_HIERARCHY.get(UserRole(user_role), 0)
    return user_value >= required_value


__all__ = ["UserRole", "role_can_access"]
