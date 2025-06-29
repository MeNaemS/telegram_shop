import pytest
from unittest.mock import AsyncMock, MagicMock
from src.config_schema import Config, Database, Telegram
from src.infrastructure.database.models.products import Category as CategoryModel, Product as ProductModel
from src.infrastructure.database.models.orders import Cart, CartItem
from src.infrastructure.database.models.users import FAQ, UserSubscription
from decimal import Decimal


@pytest.fixture
def mock_config():
    return Config(
        log_level="DEBUG",
        debug=True,
        database=Database(
            host="localhost",
            port=5432,
            name="test_db",
            user="test_user",
            password="test_pass"
        ),
        telegram=Telegram(
            token="test_token",
            chats_id=["@test_channel"]
        )
    )


@pytest.fixture
def mock_session():
    session = AsyncMock()
    session.execute = AsyncMock()
    session.commit = AsyncMock()
    session.flush = AsyncMock()
    session.refresh = AsyncMock()
    session.add = MagicMock()
    session.delete = AsyncMock()
    return session


@pytest.fixture
def sample_category():
    return CategoryModel(id=1, name="Electronics", parent_id=None)


@pytest.fixture
def sample_product():
    return ProductModel(
        id=1,
        name="iPhone",
        description="Test phone",
        image="test.jpg",
        price=Decimal("999.99"),
        category_id=1
    )


@pytest.fixture
def sample_cart():
    return Cart(id=1, user_id=12345)


@pytest.fixture
def sample_cart_item(sample_cart, sample_product):
    item = CartItem(id=1, cart_id=1, product_id=1, quantity=2)
    item.cart = sample_cart
    item.product = sample_product
    return item


@pytest.fixture
def sample_faq():
    return FAQ(id=1, question="Test question?", answer="Test answer")


@pytest.fixture
def sample_user():
    return UserSubscription(id=1, user_id=12345, is_subscribed=True)