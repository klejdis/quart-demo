from quart.testing import QuartClient


async def test_post_create(client: QuartClient, refresh_database: None) -> None:
    response = await client.post(
        "/quart-demo/posts",
        json={"name": "Test Title", "description": "Test Content"},
    )

    assert response.status_code == 200

    assert await response.json == {"success": True, "id": 1}


async def test_post_read(client: QuartClient, refresh_database: None) -> None:
    # create a post
    await client.post(
        "/quart-demo/posts",
        json={"name": "Test Title", "description": "Test Content"},
    )

    response = await client.get("/quart-demo/posts", headers={"Authorization": "token"})

    assert response.status_code == 200

    data = await response.json

    assert data == {"posts": [{"id": 1, "name": "Test Title", "description": "Test Content"}]}


async def test_post_read_one(client: QuartClient, refresh_database: None) -> None:
    # create a post
    await client.post(
        "/quart-demo/posts",
        json={"name": "Test Title", "description": "Test Content"},
    )

    response = await client.get("/quart-demo/posts/1")

    assert response.status_code == 200

    data = await response.json

    assert data == {"id": 1, "name": "Test Title", "description": "Test Content"}


async def test_post_update(client: QuartClient, refresh_database: None) -> None:
    # create a post
    await client.post(
        "/quart-demo/posts",
        json={"name": "Test Title", "description": "Test Content"},
    )

    response = await client.put(
        "/quart-demo/posts/1",
        json={"name": "New Title", "description": "New Content"},
    )

    assert response.status_code == 200

    data = await response.json

    assert data == {"id": 1, "name": "New Title", "description": "New Content"}


async def test_post_delete(client: QuartClient, refresh_database: None) -> None:
    # create a post
    await client.post(
        "/quart-demo/posts",
        json={"name": "Test Title", "description": "Test Content"},
    )

    response = await client.delete("/quart-demo/posts/1")

    assert response.status_code == 200

    data = await response.json

    assert data == {"success": True, "rowcount": 1}


async def test_post_add_comment(client: QuartClient, refresh_database: None) -> None:
    # create a post
    await client.post(
        "/quart-demo/posts",
        json={"name": "Test Title", "description": "Test Content"},
    )

    response = await client.post(
        "/quart-demo/posts/1/comments",
        json={"content": "Test Comment"},
    )

    assert response.status_code == 200

    data = await response.json

    assert data == {"success": True, "id": 1}


async def test_post_read_comments(client: QuartClient, refresh_database: None) -> None:
    # create a post
    await client.post(
        "/quart-demo/posts",
        json={"name": "Test Title", "description": "Test Content"},
    )
    # add a comment
    await client.post(
        "/quart-demo/posts/1/comments",
        json={"content": "Test Comment"},
    )

    response = await client.get("/quart-demo/posts/1/comments")

    assert response.status_code == 200

    data = await response.json

    assert data == {"comments": [{"id": 1, "content": "Test Comment"}]}


async def test_delete_comment(client: QuartClient, refresh_database: None) -> None:
    # create a post
    await client.post(
        "/quart-demo/posts",
        json={"name": "Test Title", "description": "Test Content"},
    )
    # add a comment
    await client.post(
        "/quart-demo/posts/1/comments",
        json={"content": "Test Comment"},
    )

    response = await client.delete("/quart-demo/comments/1")

    assert response.status_code == 200

    data = await response.json

    assert data == {"success": True, "rowcount": 1}
