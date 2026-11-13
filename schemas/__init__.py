"""Pydantic response contracts, one module per API under test."""

from schemas.jsonplaceholder import CommentSchema, PostSchema, UserSchema
from schemas.sentinel import ErrorSchema, HealthSchema, ScanSchema

__all__ = [
    "CommentSchema",
    "PostSchema",
    "UserSchema",
    "ErrorSchema",
    "HealthSchema",
    "ScanSchema",
]
