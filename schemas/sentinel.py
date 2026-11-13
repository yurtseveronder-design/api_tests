"""Contracts for the ai-sentinel gateway (GET /health, POST /v1/scan)."""

from typing import List, Literal

from pydantic import BaseModel, ConfigDict, Field


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class HealthSchema(_Strict):
    status: Literal["ok"]


class ScanSchema(_Strict):
    status: Literal["allowed", "blocked"]
    action: Literal["ALLOW", "BLOCK"]
    risk_score: float = Field(ge=0.0, le=1.0)
    reasons: List[str]


class ErrorSchema(_Strict):
    detail: str
