"""JSONPlaceholder fakes writes: it echoes the payload but does not persist it."""

from schemas import PostSchema


def test_create_post(api_client, post_payload):
    response = api_client.post("/posts", json=post_payload, expect_status=201)
    created = PostSchema(**response.json())
    assert created.id == 101
    assert created.title == post_payload["title"]


def test_update_post(api_client, post_payload):
    response = api_client.put("/posts/1", json={**post_payload, "id": 1}, expect_status=200)
    assert PostSchema(**response.json()).title == post_payload["title"]


def test_delete_post(api_client):
    assert api_client.delete("/posts/1", expect_status=200).json() == {}
