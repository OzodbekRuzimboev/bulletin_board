# ads/migrations/0003_add_initial_categories.py
from django.db import migrations

def create_initial_categories(apps, schema_editor):
    Category = apps.get_model('ads', 'Category')

    categories = [
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
            "keywords": "футболка, майка, рубашка, брюки, платье, куртка, джинсы, пальто, костюм, носки, кроссовки, туфли, ботинки, трусы",
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

    for cat in categories:
        Category.objects.update_or_create(
            name=cat["name"],
            defaults={
                "description": cat["description"],
                "keywords": cat["keywords"],
                "position": cat["position"],
            },
        )


def delete_initial_categories(apps, schema_editor):
    Category = apps.get_model('ads', 'Category')
    names = [
        "Недвижимость", "Работа", "Авто", "Электроника",
        "Мебель", "Одежда, обувь", "Услуги", "Другое",
    ]
    Category.objects.filter(name__in=names).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("ads", "0002_remove_ad_is_active"),
    ]

    operations = [
        migrations.RunPython(create_initial_categories, delete_initial_categories),
    ]
