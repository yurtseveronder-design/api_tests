"""Pydantic response contracts, one module per API under test."""

from schemas.jsonplaceholder import CommentSchema, PostSchema, UserSchema
from schemas.semantic import AnalyzeSchema, FilterSchema, RouteSchema, SemanticHealthSchema
from schemas.sentinel import ErrorSchema, HealthSchema, ScanSchema, SemanticSummarySchema

__all__ = [
    "CommentSchema",
    "PostSchema",
    "UserSchema",
    "AnalyzeSchema",
    "FilterSchema",
    "RouteSchema",
    "SemanticHealthSchema",
    "SemanticSummarySchema",
    "ErrorSchema",
    "HealthSchema",
    "ScanSchema",
]
