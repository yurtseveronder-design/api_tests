from schemas import CommentSchema, PostSchema


def test_list_posts_matches_contract(api_client):
    posts = api_client.get("/posts", expect_status=200).json()
    assert len(posts) == 100
    for post in posts[:10]:
        PostSchema(**post)


def test_get_single_post(api_client):
    post = PostSchema(**api_client.get("/posts/1", expect_status=200).json())
    assert post.id == 1


def test_filter_posts_by_user(api_client):
    posts = api_client.get("/posts", params={"userId": 1}, expect_status=200).json()
    assert posts and all(PostSchema(**p).userId == 1 for p in posts)


def test_nested_comments_belong_to_post(api_client):
    comments = api_client.get("/posts/1/comments", expect_status=200).json()
    assert comments
    assert all(CommentSchema(**c).postId == 1 for c in comments)
