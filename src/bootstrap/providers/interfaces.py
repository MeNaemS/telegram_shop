from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.repositories.category_repo import CategoryRepositoryInterface
from src.domain.repositories.user_repo import UserRepositoryInterface
from src.domain.repositories.faq_repo import FAQRepositoryInterface
from src.domain.repositories.product_repo import ProductRepositoryInterface
from src.domain.repositories.cart_repo import CartRepositoryInterface
from src.domain.repositories.order_repo import OrderRepositoryInterface
from src.infrastructure.database.repositories.category_repo_impl import CategoryRepositoryImpl
from src.infrastructure.database.repositories.user_repo_impl import UserRepositoryImpl
from src.infrastructure.database.repositories.faq_repo_impl import FAQRepositoryImpl
from src.infrastructure.database.repositories.product_repo_impl import ProductRepositoryImpl
from src.infrastructure.database.repositories.cart_repo_impl import CartRepositoryImpl
from src.infrastructure.database.repositories.order_repo_impl import OrderRepositoryImpl


class InterfacesProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_category_repo(self, session: AsyncSession) -> CategoryRepositoryInterface:
        return CategoryRepositoryImpl(session)

    @provide(scope=Scope.REQUEST)
    async def get_user_repo(self, session: AsyncSession) -> UserRepositoryInterface:
        return UserRepositoryImpl(session)

    @provide(scope=Scope.REQUEST)
    async def get_faq_repo(self, session: AsyncSession) -> FAQRepositoryInterface:
        return FAQRepositoryImpl(session)

    @provide(scope=Scope.REQUEST)
    async def get_product_repo(self, session: AsyncSession) -> ProductRepositoryInterface:
        return ProductRepositoryImpl(session)

    @provide(scope=Scope.REQUEST)
    async def get_cart_repo(self, session: AsyncSession) -> CartRepositoryInterface:
        return CartRepositoryImpl(session)

    @provide(scope=Scope.REQUEST)
    async def get_order_repo(self, session: AsyncSession) -> OrderRepositoryInterface:
        return OrderRepositoryImpl(session)
