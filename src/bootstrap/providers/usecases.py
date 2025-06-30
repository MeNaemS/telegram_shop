from dishka import Provider, provide, Scope
from src.application.interfaces.telegram_client import TelegramClientInterface
from src.application.usecases.telegram_subscription import TelegramSubscriptionUseCase
from src.application.usecases.register_user import RegisterUserUseCase
from src.application.usecases.get_faq import GetFAQUseCase
from src.application.usecases.get_faq_by_id import GetFAQByIdUseCase
from src.application.usecases.get_products import GetProductsUseCase
from src.application.usecases.add_to_cart import AddToCartUseCase
from src.application.usecases.get_cart import GetCartUseCase
from src.application.usecases.remove_from_cart import RemoveFromCartUseCase
from src.application.usecases.create_order import CreateOrderUseCase
from src.domain.repositories.category_repo import CategoryRepositoryInterface
from src.domain.repositories.user_repo import UserRepositoryInterface
from src.domain.repositories.faq_repo import FAQRepositoryInterface
from src.domain.repositories.product_repo import ProductRepositoryInterface
from src.domain.repositories.cart_repo import CartRepositoryInterface
from src.domain.repositories.order_repo import OrderRepositoryInterface
from src.application.interfaces.excel_client import ExcelClientInterface
from src.application.mappers.main_menu_mapper import CategoryMapper
from src.application.usecases.get_categories import GetCategoriesUseCase
from src.application.usecases.get_subcategories import GetSubcategoriesUseCase
from src.application.usecases.create_payment import CreatePaymentUseCase
from src.application.interfaces.payment_client import PaymentClientInterface


class UseCasesProvider(Provider):
    @provide(scope=Scope.APP)
    async def subscription_use_case(
        self,
        telegram_client: TelegramClientInterface
    ) -> TelegramSubscriptionUseCase:
        return TelegramSubscriptionUseCase(telegram_client)

    @provide(scope=Scope.REQUEST)
    async def register_user_use_case(
        self, user_repo: UserRepositoryInterface
    ) -> RegisterUserUseCase:
        return RegisterUserUseCase(user_repo)

    @provide(scope=Scope.REQUEST)
    async def faq_use_case(
        self, faq_repo: FAQRepositoryInterface
    ) -> GetFAQUseCase:
        return GetFAQUseCase(faq_repo)

    @provide(scope=Scope.REQUEST)
    async def faq_by_id_use_case(
        self, faq_repo: FAQRepositoryInterface
    ) -> GetFAQByIdUseCase:
        return GetFAQByIdUseCase(faq_repo)

    @provide(scope=Scope.REQUEST)
    async def categories_use_case(
        self, category_repo: CategoryRepositoryInterface, category_mapper: CategoryMapper
    ) -> GetCategoriesUseCase:
        return GetCategoriesUseCase(category_repo, category_mapper)

    @provide(scope=Scope.REQUEST)
    async def subcategories_use_case(
        self, category_repo: CategoryRepositoryInterface, category_mapper: CategoryMapper
    ) -> GetSubcategoriesUseCase:
        return GetSubcategoriesUseCase(category_repo, category_mapper)

    @provide(scope=Scope.REQUEST)
    async def products_use_case(
        self, product_repo: ProductRepositoryInterface
    ) -> GetProductsUseCase:
        return GetProductsUseCase(product_repo)

    @provide(scope=Scope.REQUEST)
    async def add_to_cart_use_case(
        self, cart_repo: CartRepositoryInterface
    ) -> AddToCartUseCase:
        return AddToCartUseCase(cart_repo)

    @provide(scope=Scope.REQUEST)
    async def get_cart_use_case(
        self, cart_repo: CartRepositoryInterface
    ) -> GetCartUseCase:
        return GetCartUseCase(cart_repo)

    @provide(scope=Scope.REQUEST)
    async def remove_from_cart_use_case(
        self, cart_repo: CartRepositoryInterface
    ) -> RemoveFromCartUseCase:
        return RemoveFromCartUseCase(cart_repo)

    @provide(scope=Scope.REQUEST)
    async def create_order_use_case(
        self, cart_repo: CartRepositoryInterface, order_repo: OrderRepositoryInterface, excel_client: ExcelClientInterface, payment_client: PaymentClientInterface
    ) -> CreateOrderUseCase:
        return CreateOrderUseCase(cart_repo, order_repo, excel_client, payment_client)

    @provide(scope=Scope.REQUEST)
    async def create_payment_use_case(
        self, cart_repo: CartRepositoryInterface, payment_client: PaymentClientInterface
    ) -> CreatePaymentUseCase:
        return CreatePaymentUseCase(cart_repo, payment_client)