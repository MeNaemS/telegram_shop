# 🤖 Telegram Shop Bot

Telegram бот для интернет-магазина с полным функционалом покупок, корзины, заказов и автоматической записью в Excel.

## 📋 Содержание

- [Особенности](#-особенности)
- [Технологии](#-технологии)
- [Структура проекта](#-структура-проекта)
- [Установка и запуск](#-установка-и-запуск)
- [Конфигурация](#️-конфигурация)
- [Использование](#-использование)
- [Разработка](#-разработка)
- [Тестирование](#-тестирование)
- [Docker](#-docker)
- [Лицензия](#-лицензия)

## ✨ Особенности

- 🛍️ **Каталог товаров**: Просмотр категорий и товаров с изображениями
- 🛒 **Корзина**: Добавление товаров, управление количеством
- 📦 **Заказы**: Полный цикл оформления заказа с контактными данными
- 📊 **Excel отчеты**: Автоматическая запись всех заказов в Excel файл
- ❓ **FAQ**: Система часто задаваемых вопросов
- 🔐 **Подписки**: Проверка подписки на каналы перед использованием
- 🎨 **Интуитивный интерфейс**: Удобная навигация с inline клавиатурой
- 🏗️ **Чистая архитектура**: Разделение на слои Domain, Application, Infrastructure

## 🛠 Технологии

- **Framework**: Aiogram 3.20.0, Python 3.13
- **База данных**: PostgreSQL с SQLAlchemy 2.0.41
- **DI контейнер**: Dishka 1.6.0
- **Конфигурация**: Dynaconf 3.2.11
- **Excel**: OpenPyXL 3.1.5
- **HTTP клиент**: aiohttp 3.11.18
- **Тестирование**: pytest 8.4.1, pytest-asyncio 0.25.0
- **Контейнеризация**: Docker & Docker Compose

## 📁 Структура проекта

```text
TelegramShop/
├── 📄 Dockerfile               # Docker конфигурация
├── 📄 requirements.txt         # Python зависимости
├── 📄 pytest.ini              # Конфигурация тестов
├── 📁 configs/                 # Конфигурационные файлы
│   ├── config.toml             # Основная конфигурация
│   └── secret.toml             # Секретные настройки (не в git)
├── 📁 tests/                   # E2E тесты
│   ├── conftest.py             # Фикстуры для тестов
│   └── e2e/                    # End-to-end тесты
│       ├── routers/            # Тесты роутеров
│       ├── usecases/           # Тесты бизнес-логики
│       └── integration/        # Интеграционные тесты
└── 📁 src/                     # Исходный код
    ├── 📄 config.py            # Загрузка конфигурации
    ├── 📄 config_schema.py     # Схема конфигурации
    ├── 📁 bootstrap/           # Инициализация приложения
    │   ├── main.py             # Точка входа
    │   ├── container.py        # DI контейнер
    │   └── providers/          # DI провайдеры
    ├── 📁 domain/              # Доменный слой
    │   ├── entities/           # Сущности
    │   └── repositories/       # Интерфейсы репозиториев
    ├── 📁 application/         # Слой приложения
    │   ├── usecases/           # Бизнес-логика
    │   ├── interfaces/         # Интерфейсы
    │   ├── dtos/               # Объекты передачи данных
    │   └── mappers/            # Мапперы
    ├── 📁 infrastructure/      # Инфраструктурный слой
    │   ├── database/           # База данных
    │   │   ├── models/         # SQLAlchemy модели
    │   │   └── repositories/   # Реализации репозиториев
    │   ├── telegram/           # Telegram клиент
    │   ├── http/               # HTTP клиенты
    │   ├── excel/              # Excel клиент
    │   └── logging/            # Логирование
    └── 📁 presentation/        # Слой представления
        └── telegram/           # Telegram интерфейс
            ├── routers/        # Обработчики команд
            ├── keyboards/      # Клавиатуры
            ├── middlewares/    # Middleware
            └── states/         # FSM состояния
```

## 🚀 Установка и запуск

### Предварительные требования

- Docker и Docker Compose
- Git

### Быстрый старт

1. **Клонирование репозитория**

   ```bash
   git clone <repository-url>
   cd TelegramShop
   ```

2. **Создание файла с секретами**

   ```bash
   # Создайте файл configs/secret.toml
   cp configs/config.toml configs/secret.toml
   ```

   Отредактируйте `configs/secret.toml`:

   ```toml
   [default.database]
   user = "your_db_user"
   password = "your_db_password"
   name = "your_db_name"
   
   [default.telegram]
   token = "your_bot_token"
   chats_id = ["@your_channel"]
   ```

3. **Запуск с Docker Compose**

   ```bash
   # Из корневой директории проекта
   docker compose up -d
   ```

4. **Проверка работы**
   - Бот будет доступен в Telegram
   - Логи: `docker compose logs -f telegram-bot`
   - Excel отчеты: `./reports/orders.xlsx`

### Альтернативный запуск (без Docker)

1. **Установка зависимостей**

   ```bash
   pip install -r requirements.txt
   ```

2. **Настройка базы данных PostgreSQL**

   ```bash
   # Создайте базу данных PostgreSQL
   createdb your_db_name
   ```

3. **Запуск бота**

   ```bash
   python -m src.bootstrap.main
   ```

## ⚙️ Конфигурация

Система использует **Dynaconf** для управления конфигурацией с поддержкой различных окружений.

### Файлы конфигурации

- `configs/config.toml` - основные настройки
- `configs/secret.toml` - секретные данные (не добавляется в git)

### Окружения

- `default` - настройки по умолчанию
- `production` - продакшн настройки

### Переменные окружения

```bash
ENV_FOR_DYNACONF=production  # Выбор окружения
```

### Пример конфигурации

```toml
[default]
log_level = "DEBUG"
debug = true

[default.database]
host = "localhost"
port = 5432
user = "postgres"
password = "password"
name = "telegram_shop"

[default.telegram]
token = "your_bot_token"
chats_id = ["@your_channel"]

[production]
log_level = "WARNING"
debug = false

[production.database]
host = "postgres"  # Docker service name
```

## 📖 Использование

### Основные команды бота

- `/start` - Запуск бота и регистрация пользователя
- **📦 Каталог** - Просмотр категорий и товаров
- **🛒 Корзина** - Управление корзиной покупок
- **❓ FAQ** - Часто задаваемые вопросы

### Процесс покупки

1. **Выбор товара**: Навигация по категориям → выбор товара
2. **Добавление в корзину**: Указание количества → добавление
3. **Оформление заказа**: Ввод контактных данных → выбор оплаты
4. **Подтверждение**: Заказ сохраняется в БД и Excel

### Excel отчеты

Все заказы автоматически записываются в файл `reports/orders.xlsx` со следующими данными:

- Дата и время заказа
- ID пользователя
- Контактная информация
- Список товаров
- Общая сумма

## 🔧 Разработка

### Архитектура

Проект следует принципам **Clean Architecture**:

- **Domain**: Бизнес-сущности и интерфейсы
- **Application**: Use Cases и бизнес-логика
- **Infrastructure**: Внешние зависимости (БД, API, файлы)
- **Presentation**: Telegram интерфейс

### Dependency Injection

Используется **Dishka** для управления зависимостями:

```python
# Пример провайдера
class UseCasesProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def create_order_use_case(
        self, cart_repo: CartRepositoryInterface, 
        order_repo: OrderRepositoryInterface,
        excel_client: ExcelClientInterface
    ) -> CreateOrderUseCase:
        return CreateOrderUseCase(cart_repo, order_repo, excel_client)
```

### Добавление новых функций

1. Создайте сущность в `domain/entities/`
2. Определите интерфейс репозитория в `domain/repositories/`
3. Реализуйте репозиторий в `infrastructure/database/repositories/`
4. Создайте Use Case в `application/usecases/`
5. Добавьте роутер в `presentation/telegram/routers/`
6. Зарегистрируйте в DI контейнере

## 🧪 Тестирование

### Структура тестов

```text
tests/
├── conftest.py                 # Базовые фикстуры
└── e2e/                       # End-to-end тесты
    ├── routers/               # Тесты use cases
    ├── usecases/              # Тесты бизнес-логики
    └── integration/           # Интеграционные тесты
```

### Запуск тестов

```bash
# Все тесты
pytest

# Конкретная категория
pytest tests/e2e/usecases/
pytest tests/e2e/integration/

# С покрытием
pytest --cov=src
```

### Примеры тестов

```python
@pytest.mark.asyncio
async def test_create_order_success(sample_cart_item):
    # Arrange
    mock_cart_repo = AsyncMock()
    mock_cart_repo.get_cart_items = AsyncMock(return_value=[sample_cart_item])
    
    use_case = CreateOrderUseCase(mock_cart_repo, mock_order_repo, mock_excel_client)
    
    # Act
    await use_case.execute(12345, "John Doe", "123 Main St", "+1234567890", "Card")
    
    # Assert
    mock_cart_repo.get_cart_items.assert_called_once_with(12345)
```

## 🐳 Docker

### Dockerfile

Приложение использует Python 3.13-slim образ с оптимизированной конфигурацией.

### Docker Compose интеграция

Бот интегрирован в общий docker-compose.yaml:

```yaml
telegram-bot:
  build: ./TelegramShop
  container_name: telegram-bot
  restart: always
  depends_on:
    - postgres
    - django
  volumes:
    - ./logs:/app/logs
    - ./reports:/app/reports
  environment:
    - ENV_FOR_DYNACONF=production
```

### Мониторинг

```bash
# Логи бота
docker compose logs -f telegram-bot

# Статус контейнеров
docker compose ps

# Перезапуск бота
docker compose restart telegram-bot
```

## 📝 Лицензия

Этот проект лицензирован под MIT License - см. файл [LICENSE](LICENSE) для деталей.
