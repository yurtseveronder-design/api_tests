from schemas import PostResponseSchema as PostSchema

def test_get_all_posts_status_and_count(api_client):
    response = api_client.get("/posts")
    assert response.status_code == 200
    posts = response.json()
    assert isinstance(posts, list)
    assert len(posts) > 0
    
    # Validate the data contract of the first post item
    validated_post = PostSchema(**posts[0])
    assert validated_post.id == posts[0]["id"]

def test_get_single_post_by_id(api_client):
    response = api_client.get("/posts/1")
    assert response.status_code == 200
    post = response.json()
    
    # Validate single post schema
    validated_post = PostSchema(**post)
    assert validated_post.id == 1