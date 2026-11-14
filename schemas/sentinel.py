"""Contracts for the ai-sentinel gateway (GET /health, POST /v1/scan)."""

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class HealthSchema(_Strict):
    status: Literal["ok"]


class SemanticSummarySchema(_Strict):
    """Present on /v1/scan responses when the gateway runs with the semantic layer."""

    intent: Optional[str] = None
    guardrail_profile: Optional[str] = None
    requires_rag: Optional[bool] = None
    sensitivity_tags: List[str] = Field(default_factory=list)
    filters: Dict[str, Any] = Field(default_factory=dict)
    engine: Optional[str] = None


class ScanSchema(_Strict):
    status: Literal["allowed", "blocked"]
    action: Literal["ALLOW", "BLOCK"]
    risk_score: float = Field(ge=0.0, le=1.0)
    reasons: List[str]
    semantic: Optional[SemanticSummarySchema] = None


class ErrorSchema(_Strict):
    detail: str
