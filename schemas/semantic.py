"""Contracts for the sentinel-semantic service."""

from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class SemanticHealthSchema(_Strict):
    status: Literal["ok"]
    service: Literal["sentinel-semantic"]
    version: str
    engine: Literal["keyword", "embedding"]


class RouteSchema(_Strict):
    primary_intent: str
    all_intents: List[str]
    confidence_scores: Dict[str, float]
    guardrail_profile: Literal["standard", "strict_financial", "strict_pii_redaction", "maximum_security_block"]
    requires_rag: bool
    sensitivity_tags: List[str]


class FilterSchema(_Strict):
    department: Optional[str] = None
    access_level: Optional[str] = None
    year: Optional[int] = Field(default=None, ge=2000, le=2099)
    tags: List[str]
    cleaned_query: str


class AnalyzeSchema(_Strict):
    route: RouteSchema
    filters: FilterSchema
    vector_db_filter: Dict[str, object]
    engine: Literal["keyword", "embedding"]
