from django.core.management.base import BaseCommand
from ads.models import Category
import logging

logger = logging.getLogger(__name__)

# --- описание катеогрий ---
CATEGORIES = [
    {
        "name": "Недвижимость",
        "description": "Дома, квартиры и земельные участки",
        "keywords": "дом, квартира, земля, недвижимость, аренда, сдача, покупка, жилье, комната, участок, ипотека",
        "position": 0,
    },
    {
        "name": "Работа",
        "description": "Объявления о работе и возможностях трудоустройства",
        "keywords": "работа, карьера, трудоустройство, вакансия, должность, найм, возможность, зарплата, резюме",
        "position": 1,
    },
    {
        "name": "Авто",
        "description": "Автомобили, мотоциклы и другие транспортные средства",
        "keywords": "машина, автомобиль, мотоцикл, велосипед, авто, транспорт, фургон, джип, седан, тачка, колеса",
        "position": 2,
    },
    {
        "name": "Электроника",
        "description": "Электронные устройства и гаджеты",
        "keywords": "телефон, ноутбук, компьютер, гаджет, устройство, телевизор, планшет, камера, наушники, колонка, смартфон",
        "position": 3,
    },
    {
        "name": "Мебель",
        "description": "Домашняя и офисная мебель",
        "keywords": "стул, стол, кровать, диван, шкаф, полка, комод, тумба, мебель, гарнитур",
        "position": 4,
    },
    {
        "name": "Одежда, обувь",
        "description": "Одежда, обувь и аксессуары",
        "keywords": "футболка, майка, рубашка, брюки, платье, куртка, обувь, шляпа, аксессуар, джинсы, пальто, костюм, носки, кроссовки, туфли, ботинки, трусы",
        "position": 5,
    },
    {
        "name": "Услуги",
        "description": "Профессиональные и личные услуги",
        "keywords": "ремонт, уборка, дизайн, консультация, помощь, услуга, профессиональный, обслуживание, мастер",
        "position": 6,
    },
    {
        "name": "Другое",
        "description": "Разные предметы, которые не подходят к другим категориям",
        "keywords": "разное, другое, прочее, различное",
        "position": 7,
    },
]


class Command(BaseCommand):
    help = "Создаёт или обновляет стандартные категории"

    def handle(self, *args, **options):
        self.stdout.write("🛠  Ensuring standard categories…")

        # Создаём или обновляем каждую нужную категорию
        for cat in CATEGORIES:
            obj, created = Category.objects.update_or_create(
                name=cat["name"],
                defaults={
                    "description": cat["description"],
                    "position":    cat["position"],
                    "keywords":    cat["keywords"],
                },
            )
            action = "➕ создана" if created else "↺ обновлена"
            self.stdout.write(f"  {action}: {obj.name}")

        self.stdout.write(self.style.SUCCESS("✅ Категории в порядке!"))
