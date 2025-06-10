from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Category

async def init_categories(session: AsyncSession):
    """Инициализация категорий постов"""
    categories = [
        "Отсутствует", "Автомобили", "Бизнес", "Дом и сад", "Еда и напитки",
        "Животные", "Игры", "Искусство", "История", "Книги", "Личное развитие",
        "Мода", "Музыка", "Наука", "Образование", "Психология", "Путешествия",
        "Развлечения", "Спорт", "Технологии", "Фильмы", "Финансы", "Фотография",
        "Политика", "Здоровье"
    ]

    existing_categories = await session.execute(text("SELECT name FROM categories"))
    existing_categories = {row[0] for row in existing_categories.fetchall()}

    new_categories = [Category(name=name) for name in categories if name not in existing_categories]

    if new_categories:
        session.add_all(new_categories)
        await session.commit()
        print("Категории добавлены в базу данных.")
    else:
        print("Все категории уже существуют.") 