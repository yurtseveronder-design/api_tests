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
