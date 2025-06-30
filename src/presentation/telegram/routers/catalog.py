from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from dishka.integrations.aiogram import inject, FromDishka
from src.application.usecases.get_categories import GetCategoriesUseCase
from src.application.usecases.get_subcategories import GetSubcategoriesUseCase
from src.application.usecases.get_products import GetProductsUseCase
from src.application.dtos.main_menu import CategoryDTO
from src.presentation.telegram.keyboards.paginated_keyboard import create_paginated_keyboard
from src.presentation.telegram.keyboards.product_keyboard import create_product_keyboard
from src.presentation.telegram.services.product_service import ProductService

catalog_router: Router = Router(name=__name__)


@catalog_router.callback_query(F.data.regexp(r"menu_subcatalog_\d+_\d+"))
@inject
async def handle_subcatalog(
    callback: CallbackQuery,
    get_subcategories_use_case: FromDishka[GetSubcategoriesUseCase]
):
    parts = callback.data.split("_")
    parent_id = int(parts[2])
    page = int(parts[3])
    category_inf: CategoryDTO = await get_subcategories_use_case.execute(parent_id, page)
    keyboard: InlineKeyboardMarkup = await create_paginated_keyboard(category_inf, page, "subcatalog", parent_id)
    
    text = "📦 Подкатегории:" if category_inf.items else "📦 Подкатегории отсутствуют"
    
    try:
        await callback.message.edit_text(text, reply_markup=keyboard)
    except Exception:
        await callback.answer()


@catalog_router.callback_query(F.data.startswith("menu_catalog_"))
@inject
async def handle_catalog(
    callback: CallbackQuery,
    get_categories_use_case: FromDishka[GetCategoriesUseCase]
):
    page: int = int(callback.data.split("_")[-1])
    category_inf: CategoryDTO = await get_categories_use_case.execute(page)
    keyboard: InlineKeyboardMarkup = await create_paginated_keyboard(category_inf, page, "catalog")
    
    if callback.message.photo:
        await callback.message.delete()
        await callback.bot.send_message(
            chat_id=callback.message.chat.id,
            text="📦 Каталог товаров:",
            reply_markup=keyboard
        )
    else:
        await callback.message.edit_text("📦 Каталог товаров:", reply_markup=keyboard)


@catalog_router.callback_query(F.data.startswith("products_"))
@inject
async def handle_products(
    callback: CallbackQuery,
    get_products_use_case: FromDishka[GetProductsUseCase],
    product_service: FromDishka[ProductService]
):
    parts = callback.data.split("_")
    category_id = int(parts[1])
    current_index = int(parts[2])
    
    products = await get_products_use_case.execute(category_id)
    if not products:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_main")]
        ])
        await callback.message.edit_text("В этой категории пока нет товаров", reply_markup=keyboard)
        return
    
    product = products[current_index]
    text = f"🛍️ {product.name}\n\n📝 {product.description or 'Описание отсутствует'}\n\n💰 Цена: {product.price} руб."
    
    keyboard = await create_product_keyboard(products, current_index, category_id)
    
    if not await product_service.send_product_with_image(callback, product, text, keyboard):
        await callback.message.edit_text(text, reply_markup=keyboard)


@catalog_router.callback_query(F.data.startswith("product_"))
@inject
async def handle_product_navigation(
    callback: CallbackQuery,
    get_products_use_case: FromDishka[GetProductsUseCase],
    product_service: FromDishka[ProductService]
):
    parts = callback.data.split("_")
    category_id = int(parts[1])
    current_index = int(parts[2])
    
    products = await get_products_use_case.execute(category_id)
    product = products[current_index]
    text = f"🛍️ {product.name}\n\n📝 {product.description or 'Описание отсутствует'}\n\n💰 Цена: {product.price} руб."
    
    keyboard = await create_product_keyboard(products, current_index, category_id)
    
    if not await product_service.send_product_with_image(callback, product, text, keyboard):
        await callback.message.edit_text(text, reply_markup=keyboard)
