from beelearn.utils import file_to_image_field
from .models import Tag, Category


def seed_categories():
    categories = []

    categories.append(
        Category(
            name="Web development",
            icon="web",
        ),
    )
    categories.append(
        Category(
            name="Mobile development",
            icon="mobile",
        )
    )
    categories.append(
        Category(
            name="Game development",
            icon="game",
        ),
    )
    categories.append(
        Category(
            name="Hardware",
            icon="hardware",
        ),
    )
    categories.append(
        Category(
            name="Database",
            icon="database",
        ),
    )
    categories.append(
        Category(
            name="Data Science",
            icon="statistic",
        ),
    )
    categories.append(
        Category(
            name="Content writing",
            icon="content",
        ),
    )
    categories.append(
        Category(
            name="Cyber security",
            icon="security",
        ),
    )
    categories.append(
        Category(
            name="Argument reality",
            icon="ar",
        ),
    )
    categories.append(
        Category(
            name="Cloud Ops",
            icon="cloud_ops",
        ),
    )
    categories.append(
        Category(
            name="Blockchain",
            icon="blockchain",
        ),
    )

    for category in categories:
        category: Category = category
        if not Category.objects.filter(name=category.name).exists():
            category.icon = file_to_image_field(
                f"metadata/static/icons/{category.icon}.svg"
            )

    Category.objects.bulk_create(
        categories,
        ignore_conflicts=True,
    )


def seed_tags():
    tags = [
        "CSS",
        "JavaScript",
        "HTML",
        "React",
        "Svelte",
        "Vue",
        "Angular",
    ]

    category = Category.objects.get(name="Web development")
    Tag.objects.bulk_create(
        list(
            map(
                lambda name: Tag(name=name, category=category),
                tags,
            ),
        ),
        ignore_conflicts=True,
    )

    tags = [
        "Flutter",
        "React native",
        "Java",
        "Kotlin",
        "Swift",
        "Ionic",
        "Objective-c",
    ]

    category = Category.objects.get(name="Mobile development")
    Tag.objects.bulk_create(
        list(
            map(
                lambda name: Tag(name=name, category=category),
                tags,
            ),
        ),
        ignore_conflicts=True,
    )

    tags = [
        "Unity",
    ]

    category = Category.objects.get(name="Game development")
    Tag.objects.bulk_create(
        list(
            map(
                lambda name: Tag(name=name, category=category),
                tags,
            ),
        ),
        ignore_conflicts=True,
    )

    tags = [
        "SQL",
        "MongoDB",
        "Postgresql",
    ]

    category = Category.objects.get(name="Database")
    Tag.objects.bulk_create(
        list(
            map(
                lambda name: Tag(name=name, category=category),
                tags,
            ),
        ),
        ignore_conflicts=True,
    )

    tags = [
        "R",
        "Python",
        "Machine Learning",
        "Artificial Intelligence",
    ]

    category = Category.objects.get(name="Data Science")
    Tag.objects.bulk_create(
        list(
            map(
                lambda name: Tag(name=name, category=category),
                tags,
            ),
        ),
        ignore_conflicts=True,
    )

    tags = [
        "web3",
        "solidity",
        "hardhat",
        "mining",
        "trading",
        "finance",
        "smart contract",
        "altcoin",
        "bitcoin",
        "dapp",
    ]

    category = Category.objects.get(name="Blockchain")
    Tag.objects.bulk_create(
        list(
            map(
                lambda name: Tag(name=name, category=category),
                tags,
            ),
        ),
        ignore_conflicts=True,
    )


def up():
    seed_categories()
    seed_tags()


def down():
    Tag.objects.all().delete()
    Category.objects.all().delete()
