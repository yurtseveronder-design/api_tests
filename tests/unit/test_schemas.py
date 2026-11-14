"""The contracts must accept good data and reject drift, otherwise they prove nothing."""

import pytest
from pydantic import ValidationError

from schemas import CommentSchema, ErrorSchema, HealthSchema, PostSchema, ScanSchema

POST = {"userId": 1, "id": 1, "title": "t", "body": "b"}


def test_post_accepts_valid():
    assert PostSchema(**POST).id == 1


@pytest.mark.parametrize("mutation", [
    lambda d: d.pop("title"),                 # missing field
    lambda d: d.update(id="abc"),             # wrong type
    lambda d: d.update(surprise="field"),     # unexpected field
])
def test_post_rejects_drift(mutation):
    data = dict(POST)
    mutation(data)
    with pytest.raises(ValidationError):
        PostSchema(**data)


def test_comment_rejects_bad_email():
    with pytest.raises(ValidationError):
        CommentSchema(postId=1, id=1, name="n", email="not-an-email", body="b")


def test_scan_schema():
    ok = ScanSchema(status="blocked", action="BLOCK", risk_score=0.9, reasons=["x"])
    assert ok.action == "BLOCK"
    for bad in [
        dict(status="maybe", action="BLOCK", risk_score=0.9, reasons=[]),
        dict(status="allowed", action="ALLOW", risk_score=1.5, reasons=[]),
        dict(status="allowed", action="ALLOW", risk_score=0.0),
    ]:
        with pytest.raises(ValidationError):
            ScanSchema(**bad)


def test_health_and_error_schema():
    assert HealthSchema(status="ok")
    with pytest.raises(ValidationError):
        HealthSchema(status="down")
    assert ErrorSchema(detail="x").detail == "x"


def test_scan_schema_accepts_optional_semantic_block():
    from schemas import ScanSchema

    base = dict(status="allowed", action="ALLOW", risk_score=0.0, reasons=[])
    assert ScanSchema(**base).semantic is None
    with_semantic = ScanSchema(**base, semantic={"intent": "general_chat", "guardrail_profile": "standard",
                                                 "requires_rag": False, "sensitivity_tags": [], "filters": {},
                                                 "engine": "keyword"})
    assert with_semantic.semantic.intent == "general_chat"
    with pytest.raises(ValidationError):
        ScanSchema(**base, semantic={"intent": "x", "unexpected": 1})


def test_semantic_contracts_reject_unknown_profile_and_engine():
    from schemas import RouteSchema, SemanticHealthSchema

    route = dict(primary_intent="x", all_intents=["x"], confidence_scores={"x": 0.1},
                 guardrail_profile="standard", requires_rag=False, sensitivity_tags=[])
    assert RouteSchema(**route)
    with pytest.raises(ValidationError):
        RouteSchema(**{**route, "guardrail_profile": "lenient"})
    with pytest.raises(ValidationError):
        SemanticHealthSchema(status="ok", service="sentinel-semantic", version="1", engine="magic")
