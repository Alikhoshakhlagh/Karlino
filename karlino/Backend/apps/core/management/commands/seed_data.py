import random

from django.core.management.base import BaseCommand
from faker import Faker

from ....accounts.models import User
from ....categories.models import Category
from ....skills.models import Skill
from ....companies.models import Company
from ....projects.models import Project
from ....applications.models import Application
from ....favorites.models import Favorite
from django.utils.text import slugify


fake = Faker()


def make_slug(value):

    return slugify(
        value,
        allow_unicode=True,
    )


class Command(BaseCommand):

    help = 'Seed fake data'

    def handle(self, *args, **kwargs):

        self.stdout.write(self.style.WARNING('Deleting old data...'))

        Favorite.objects.all().delete()
        Application.objects.all().delete()
        Project.objects.all().delete()
        Company.objects.all().delete()
        Skill.objects.all().delete()
        Category.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        self.stdout.write(self.style.SUCCESS('Old data deleted.'))

        # -----------------------------------
        # Categories
        # -----------------------------------

        category_data = [
            {
                'name': 'هوش مصنوعی',
                'icon': 'fa-solid fa-robot',
            },

            {
                'name': 'طراحی وب',
                'icon': 'fa-solid fa-globe',
            },

            {
                'name': 'بک‌اند',
                'icon': 'fa-solid fa-server',
            },

            {
                'name': 'فرانت‌اند',
                'icon': 'fa-solid fa-code',
            },

            {
                'name': 'اپلیکیشن موبایل',
                'icon': 'fa-solid fa-mobile-screen',
            },

            {
                'name': 'DevOps و زیرساخت',
                'icon': 'fa-solid fa-cloud',
            },

            {
                'name': 'رابط کاربری و تجربه کاربری',
                'icon': 'fa-solid fa-palette',
            },

            {
                'name': 'علم داده و تحلیل',
                'icon': 'fa-solid fa-chart-line',
            },
        ]

        categories = []

        for item in category_data:

            category = Category.objects.create(
                name=item['name'],
                slug=make_slug(item['name']),
                icon=item['icon'],
            )

            categories.append(category)

        self.stdout.write(self.style.SUCCESS('Categories created.'))

        # -----------------------------------
        # Skills
        # -----------------------------------

        skill_names = [
            'Python',
            'Django',
            'FastAPI',
            'React',
            'Vue',
            'Docker',
            'Kubernetes',
            'TensorFlow',
            'PyTorch',
            'Linux',
            'Redis',
            'Celery',
            'SQL Server',
            'PostgreSQL',
            'JavaScript',
            'TypeScript',
            'SASS',
            'Tailwind',
        ]

        skills = []

        for name in skill_names:

            skill = Skill.objects.create(
                name=name,
                slug=name.lower().replace(' ', '-'),
            )

            skills.append(skill)

        self.stdout.write(self.style.SUCCESS('Skills created.'))

        # -----------------------------------
        # Users
        # -----------------------------------

        users = []

        for i in range(20):

            gender = random.choice([
                User.Gender.MALE,
                User.Gender.FEMALE,
            ])

            user = User.objects.create_user(

                email=f'user{i}@test.com',

                first_name=fake.first_name(),

                last_name=fake.last_name(),

                date_of_birth=fake.date_of_birth(
                    minimum_age=18,
                    maximum_age=45,
                ),

                gender=gender,

                phone=f'09{random.randint(100000000, 999999999)}',

                password='Test12345'
            )

            users.append(user)

        self.stdout.write(self.style.SUCCESS('Users created.'))

        # -----------------------------------
        # Companies
        # -----------------------------------

        companies = []

        company_users = random.sample(users, 8)

        for user in company_users:

            company = Company.objects.create(
                owner=user,

                name=fake.company(),

                description=fake.text(max_nb_chars=200),

                website=fake.url(),

                phone=f'09{random.randint(100000000, 999999999)}',

                address=fake.address(),

                is_verified=random.choice([True, False]),
            )

            companies.append(company)

        self.stdout.write(self.style.SUCCESS('Companies created.'))

        # -----------------------------------
        # Projects
        # -----------------------------------

        projects = []

        for i in range(50):

            creator = random.choice(users)

            user_company = getattr(
                creator,
                'company',
                None
            )

            use_company = (
                user_company is not None
                and random.choice([True, False])
            )

            primary_category = random.choice(categories)

            extra_categories = random.sample(
                categories,
                random.randint(1, 3)
            )

            project = Project.objects.create(

                creator=creator,

                owner_type=(
                    Project.OwnerType.COMPANY
                    if use_company
                    else Project.OwnerType.PERSONAL
                ),

                company=(
                    user_company
                    if use_company
                    else None
                ),

                primary_category=primary_category,

                title=fake.sentence(nb_words=5),

                description=fake.text(max_nb_chars=1000),

                budget_min=random.randint(100, 1000),

                budget_max=random.randint(1500, 10000),

                location=fake.city(),

                deadline=fake.future_date(),

                status=random.choice([
                    Project.Status.ACTIVE,
                    Project.Status.ACTIVE,
                    Project.Status.ACTIVE,
                    Project.Status.CLOSED,
                ]),
            )

            project.categories.set(
                list(set(extra_categories + [primary_category]))
            )

            selected_skills = random.sample(
                skills,
                random.randint(2, 6)
            )

            project.skills.set(selected_skills)

            projects.append(project)

        self.stdout.write(self.style.SUCCESS('Projects created.'))

        # -----------------------------------
        # Applications
        # -----------------------------------

        applications_count = 0

        for project in projects:

            applicants = random.sample(
                users,
                random.randint(1, 5)
            )

            for applicant in applicants:

                if applicant.id == project.creator_id:
                    continue

                if (
                    project.company
                    and project.company.owner_id == applicant.id
                ):
                    continue

                exists = Application.objects.filter(
                    project=project,
                    applicant=applicant
                ).exists()

                if exists:
                    continue

                Application.objects.create(
                    project=project,

                    applicant=applicant,

                    cover_letter=fake.text(
                        max_nb_chars=300
                    ),

                    proposed_price=random.randint(
                        100,
                        10000
                    ),

                    status=random.choice([
                        Application.Status.PENDING,
                        Application.Status.ACCEPTED,
                        Application.Status.REJECTED,
                    ])
                )

                applications_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'{applications_count} applications created.'
            )
        )

        # -----------------------------------
        # Favorites
        # -----------------------------------

        favorites_count = 0

        for user in users:

            fav_projects = random.sample(
                projects,
                random.randint(2, 8)
            )

            for project in fav_projects:

                exists = Favorite.objects.filter(
                    user=user,
                    project=project
                ).exists()

                if exists:
                    continue

                Favorite.objects.create(
                    user=user,
                    project=project
                )

                favorites_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'{favorites_count} favorites created.'
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                'FAKE DATA CREATED SUCCESSFULLY'
            )
        )