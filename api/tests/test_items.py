import httpx
import pytest
from playwright.sync_api import Page

from demo.models import Item


@pytest.fixture
def some_items(transactional_db):
    return [
        Item.objects.create(name="Foo"),
        Item.objects.create(name="Bar"),
    ]


@pytest.mark.django_db(transaction=True)
def test_content(front_server, some_items, page: Page):
    page.goto(str(httpx.URL(front_server).join("/")))

    for item in some_items:
        item_name_escaped = repr(item.name)[1:-1]
        assert (
            page.locator(f"li:has-text('{item.id}: {item_name_escaped}')").count() == 1
        )
