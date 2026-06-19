import random
from datetime import timedelta

from faker import Faker
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.accounts.models import User
from apps.applications.models import Application
from apps.bids.models import Bid
from apps.categories.models import Category
from apps.companies.models import Company
from apps.favorites.models import Favorite
from apps.projects.models import Project, ProjectReview
from apps.skills.models import Skill


fake = Faker('fa_IR')


def get_user_company(user):
    try:
        return user.company
    except (Company.DoesNotExist, AttributeError):
        return None


def generate_budget(project_mode, category_slug):
    if project_mode == Project.ProjectMode.SIMPLE:
        base_min = random.choice([
            1_500_000,
            2_500_000,
            3_500_000,
            5_000_000,
            7_500_000,
        ])
        spread = random.choice([
            1_000_000,
            2_000_000,
            3_000_000,
            5_000_000,
        ])
    else:
        base_min = random.choice([
            5_000_000,
            10_000_000,
            15_000_000,
            20_000_000,
            30_000_000,
            40_000_000,
        ])
        spread = random.choice([
            5_000_000,
            10_000_000,
            15_000_000,
            20_000_000,
        ])

    if category_slug in {
        'ai-machine-learning',
        'data-science-data-analysis',
        'cyber-security',
        'devops-cloud-infrastructure',
    }:
        base_min += random.choice([5_000_000, 10_000_000])
        spread += random.choice([5_000_000, 10_000_000])

    budget_min = base_min
    budget_max = base_min + spread

    return budget_min, budget_max


def pick_expert_for_category(category, experts, expert_category_map):
    eligible_experts = [
        expert
        for expert in experts
        if category.id in expert_category_map.get(expert.id, set())
    ]
    return random.choice(eligible_experts or experts)


def create_project_review(project, expert, review_status, comment):
    ProjectReview.objects.create(
        project=project,
        expert=expert,
        status=review_status,
        comment=comment,
    )

    project.review_status = review_status
    project.reviewed_by = expert
    project.reviewed_at = timezone.now()

    if review_status == Project.ReviewStatus.APPROVED:
        project.status = Project.Status.ACTIVE
    elif review_status == Project.ReviewStatus.REJECTED:
        project.status = Project.Status.ARCHIVED
    elif review_status == Project.ReviewStatus.NEEDS_REVISION:
        project.status = Project.Status.DRAFT

    project.save(update_fields=[
        'review_status',
        'reviewed_by',
        'reviewed_at',
        'status',
    ])


class Command(BaseCommand):
    help = 'Seed fake data'

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            self.stdout.write(self.style.WARNING('Deleting old data...'))

            Favorite.objects.all().delete()
            Application.objects.all().delete()
            Bid.objects.all().delete()
            ProjectReview.objects.all().delete()
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
                    'name': 'برنامه‌نویسی و توسعه وب',
                    'slug': 'programming-web-development',
                    'icon': 'fa-solid fa-code',
                },
                {
                    'name': 'طراحی رابط کاربری و تجربه کاربری',
                    'slug': 'ui-ux-design',
                    'icon': 'fa-solid fa-palette',
                },
                {
                    'name': 'توسعه اپلیکیشن موبایل',
                    'slug': 'mobile-app-development',
                    'icon': 'fa-solid fa-mobile-screen',
                },
                {
                    'name': 'هوش مصنوعی و یادگیری ماشین',
                    'slug': 'ai-machine-learning',
                    'icon': 'fa-solid fa-robot',
                },
                {
                    'name': 'علم داده و تحلیل داده',
                    'slug': 'data-science-data-analysis',
                    'icon': 'fa-solid fa-chart-line',
                },
                {
                    'name': 'بک‌اند و پایگاه داده',
                    'slug': 'backend-database',
                    'icon': 'fa-solid fa-server',
                },
                {
                    'name': 'DevOps و زیرساخت ابری',
                    'slug': 'devops-cloud-infrastructure',
                    'icon': 'fa-solid fa-cloud',
                },
                {
                    'name': 'امنیت سایبری',
                    'slug': 'cyber-security',
                    'icon': 'fa-solid fa-shield-halved',
                },
                {
                    'name': 'طراحی گرافیک',
                    'slug': 'graphic-design',
                    'icon': 'fa-solid fa-pen-ruler',
                },
                {
                    'name': 'تولید محتوا و کپی‌رایتینگ',
                    'slug': 'content-writing-copywriting',
                    'icon': 'fa-solid fa-pen-to-square',
                },
                {
                    'name': 'ترجمه و زبان',
                    'slug': 'translation-language',
                    'icon': 'fa-solid fa-language',
                },
                {
                    'name': 'دیجیتال مارکتینگ و سئو',
                    'slug': 'digital-marketing-seo',
                    'icon': 'fa-solid fa-bullhorn',
                },
                {
                    'name': 'تدوین ویدئو و موشن گرافیک',
                    'slug': 'video-editing-motion-graphics',
                    'icon': 'fa-solid fa-video',
                },
                {
                    'name': 'عکاسی و ویرایش تصویر',
                    'slug': 'photography-image-editing',
                    'icon': 'fa-solid fa-camera',
                },
                {
                    'name': 'ورود داده و امور اداری',
                    'slug': 'data-entry-office-work',
                    'icon': 'fa-solid fa-keyboard',
                },
                {
                    'name': 'حسابداری و امور مالی',
                    'slug': 'accounting-finance',
                    'icon': 'fa-solid fa-calculator',
                },
                {
                    'name': 'مشاوره کسب‌وکار',
                    'slug': 'business-consulting',
                    'icon': 'fa-solid fa-briefcase',
                },
                {
                    'name': 'پشتیبانی و خدمات مشتریان',
                    'slug': 'customer-support',
                    'icon': 'fa-solid fa-headset',
                },
            ]

            categories = []
            category_by_slug = {}

            for item in category_data:
                category = Category.objects.create(
                    name=item['name'],
                    slug=item['slug'],
                    icon=item['icon'],
                )
                categories.append(category)
                category_by_slug[item['slug']] = category

            self.stdout.write(self.style.SUCCESS('Categories created.'))

            # -----------------------------------
            # Skills
            # -----------------------------------

            skill_data = [
                {'name': 'Python', 'slug': 'python'},
                {'name': 'Django', 'slug': 'django'},
                {'name': 'FastAPI', 'slug': 'fastapi'},
                {'name': 'React', 'slug': 'react'},
                {'name': 'Vue', 'slug': 'vue'},
                {'name': 'Next.js', 'slug': 'nextjs'},
                {'name': 'Docker', 'slug': 'docker'},
                {'name': 'Kubernetes', 'slug': 'kubernetes'},
                {'name': 'TensorFlow', 'slug': 'tensorflow'},
                {'name': 'PyTorch', 'slug': 'pytorch'},
                {'name': 'Linux', 'slug': 'linux'},
                {'name': 'Redis', 'slug': 'redis'},
                {'name': 'Celery', 'slug': 'celery'},
                {'name': 'SQL Server', 'slug': 'sql-server'},
                {'name': 'PostgreSQL', 'slug': 'postgresql'},
                {'name': 'JavaScript', 'slug': 'javascript'},
                {'name': 'TypeScript', 'slug': 'typescript'},
                {'name': 'SASS', 'slug': 'sass'},
                {'name': 'Tailwind CSS', 'slug': 'tailwind-css'},
                {'name': 'Figma', 'slug': 'figma'},
                {'name': 'WordPress', 'slug': 'wordpress'},
                {'name': 'SEO', 'slug': 'seo'},
                {'name': 'Copywriting', 'slug': 'copywriting'},
                {'name': 'Excel', 'slug': 'excel'},
                {'name': 'PowerPoint', 'slug': 'powerpoint'},
                {'name': 'Content Writing', 'slug': 'content-writing'},
                {'name': 'Communication', 'slug': 'communication'},
            ]

            skills = []

            for item in skill_data:
                skill = Skill.objects.create(
                    name=item['name'],
                    slug=item['slug'],
                )
                skills.append(skill)

            self.stdout.write(self.style.SUCCESS('Skills created.'))

            # -----------------------------------
            # Users
            # -----------------------------------

            users = []

            for i in range(24):
                gender = random.choice([
                    User.Gender.MALE,
                    User.Gender.FEMALE,
                ])

                user = User.objects.create_user(
                    email=f'user{i + 1}@test.com',
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    date_of_birth=fake.date_of_birth(
                        minimum_age=18,
                        maximum_age=50,
                    ),
                    gender=gender,
                    phone=f'09{900000000 + i:09d}',
                    password='Test12345',
                )
                users.append(user)

            self.stdout.write(self.style.SUCCESS('Users created.'))

            # -----------------------------------
            # Experts
            # -----------------------------------

            expert_category_groups = [
                [
                    'programming-web-development',
                    'backend-database',
                    'devops-cloud-infrastructure',
                    'cyber-security',
                ],
                [
                    'ai-machine-learning',
                    'data-science-data-analysis',
                    'mobile-app-development',
                ],
                [
                    'ui-ux-design',
                    'graphic-design',
                    'video-editing-motion-graphics',
                    'photography-image-editing',
                ],
                [
                    'content-writing-copywriting',
                    'translation-language',
                    'digital-marketing-seo',
                    'accounting-finance',
                    'business-consulting',
                    'customer-support',
                    'data-entry-office-work',
                ],
            ]

            expert_users = random.sample(users, 4)

            for expert, group in zip(expert_users, expert_category_groups):
                expert.is_expert = True
                expert.save(update_fields=['is_expert'])
                expert.expert_categories.set(
                    [category_by_slug[slug] for slug in group]
                )

            expert_category_map = {
                expert.id: {
                    category.id
                    for category in expert.expert_categories.all()
                }
                for expert in expert_users
            }

            self.stdout.write(self.style.SUCCESS('Experts created.'))

            # -----------------------------------
            # Companies
            # -----------------------------------

            companies = []
            company_owners = random.sample(users, 6)

            for index, owner in enumerate(company_owners, start=1):
                company = Company.objects.create(
                    owner=owner,
                    name=fake.company(),
                    description=fake.text(max_nb_chars=220),
                    website=f'https://company{index}.example.com',
                    phone=f'09{910000000 + index:09d}',
                    address=fake.address(),
                    is_verified=random.choice([True, False]),
                )
                companies.append(company)

            self.stdout.write(self.style.SUCCESS('Companies created.'))

            # -----------------------------------
            # Projects
            # -----------------------------------

            project_titles = [
                'طراحی سایت فروشگاهی با پنل مدیریت',
                'ساخت API احراز هویت و ثبت نام',
                'توسعه داشبورد مدیریت سفارش‌ها',
                'پیاده‌سازی سیستم فیلتر و جستجو',
                'ساخت اپلیکیشن مدیریت وظایف',
                'طراحی و توسعه سایت معرفی شرکت',
                'پیاده‌سازی ماژول درخواست پروژه',
                'ساخت پنل کارفرما و فریلنسر',
                'توسعه بخش علاقه‌مندی‌ها و درخواست‌ها',
                'پیاده‌سازی داشبورد آماری',
                'ساخت سرویس تحلیل داده و گزارش',
                'توسعه سامانه رزرو آنلاین',
                'طراحی فرانت‌اند واکنش‌گرا',
                'اتصال پروژه به SQL Server',
                'توسعه API مناقصه و پیشنهاد',
                'ساخت سیستم دسته‌بندی پروژه‌ها',
                'طراحی اپ موبایل برای سفارش آنلاین',
                'پیاده‌سازی موتور توصیه‌گر ساده',
                'تولید محتوای سئو برای صفحات سایت',
                'طراحی کمپین دیجیتال مارکتینگ',
                'تدوین ویدئو تبلیغاتی کوتاه',
                'ورود اطلاعات و مدیریت اکسل',
                'مشاوره مالی و حسابداری',
                'پشتیبانی آنلاین مشتریان',
            ]

            project_comments_approved = [
                'پروژه از نظر ساختار و جزئیات قابل پذیرش است.',
                'اطلاعات پروژه کامل است و می‌تواند منتشر شود.',
                'پروژه تایید شد و آماده نمایش در سایت است.',
            ]

            project_comments_revision = [
                'بودجه پروژه باید دقیق‌تر مشخص شود.',
                'توضیحات پروژه نیاز به تکمیل دارد.',
                'لطفاً جزئیات فنی و خروجی مورد انتظار را واضح‌تر بنویسید.',
                'فایل‌ها و اطلاعات تکمیلی را اضافه کنید.',
            ]

            project_comments_rejected = [
                'پروژه با قوانین پلتفرم سازگار نیست.',
                'شرح پروژه مبهم است و قابل انتشار نیست.',
                'این پروژه در وضعیت فعلی قابل تایید نیست.',
            ]

            projects = []

            for i in range(30):
                creator = random.choice(users)
                user_company = get_user_company(creator)

                use_company = (
                    user_company is not None
                    and random.choice([True, False])
                )

                primary_category = random.choice(categories)

                extra_categories = random.sample(
                    [c for c in categories if c != primary_category],
                    random.randint(1, 3),
                )

                project_mode = random.choice([
                    Project.ProjectMode.SIMPLE,
                    Project.ProjectMode.TENDER,
                ])

                review_status = random.choices(
                    [
                        Project.ReviewStatus.PENDING,
                        Project.ReviewStatus.APPROVED,
                        Project.ReviewStatus.NEEDS_REVISION,
                        Project.ReviewStatus.REJECTED,
                    ],
                    weights=[2, 6, 1, 1],
                    k=1,
                )[0]

                budget_min, budget_max = generate_budget(
                    project_mode,
                    primary_category.slug,
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
                    title=random.choice(project_titles),
                    description=fake.text(max_nb_chars=1000),
                    budget_min=budget_min,
                    budget_max=budget_max,
                    location=fake.city(),
                    deadline=fake.future_date(),
                    status=(
                        Project.Status.DRAFT
                        if review_status in [
                            Project.ReviewStatus.PENDING,
                            Project.ReviewStatus.NEEDS_REVISION,
                        ]
                        else (
                            Project.Status.ACTIVE
                            if review_status == Project.ReviewStatus.APPROVED
                            else Project.Status.ARCHIVED
                        )
                    ),
                    project_mode=project_mode,
                    review_status=review_status,
                )

                project.categories.set(
                    list(
                        {
                            cat.id: cat
                            for cat in [primary_category, *extra_categories]
                        }.values()
                    )
                )

                selected_skills = random.sample(
                    skills,
                    random.randint(2, 6),
                )
                project.skills.set(selected_skills)

                # backdate project age a bit for UI variety
                Project.objects.filter(pk=project.pk).update(
                    created_at=timezone.now() - timedelta(days=random.randint(0, 35))
                )

                # create review history for reviewed projects
                if review_status != Project.ReviewStatus.PENDING:
                    expert = pick_expert_for_category(
                        primary_category,
                        expert_users,
                        expert_category_map,
                    )

                    if (
                        review_status == Project.ReviewStatus.APPROVED
                        and random.random() < 0.25
                    ):
                        first_expert = pick_expert_for_category(
                            primary_category,
                            expert_users,
                            expert_category_map,
                        )
                        create_project_review(
                            project=project,
                            expert=first_expert,
                            review_status=Project.ReviewStatus.NEEDS_REVISION,
                            comment=random.choice(project_comments_revision),
                        )

                        second_expert = pick_expert_for_category(
                            primary_category,
                            expert_users,
                            expert_category_map,
                        )
                        create_project_review(
                            project=project,
                            expert=second_expert,
                            review_status=Project.ReviewStatus.APPROVED,
                            comment=random.choice(project_comments_approved),
                        )
                    else:
                        create_project_review(
                            project=project,
                            expert=expert,
                            review_status=review_status,
                            comment=random.choice(
                                project_comments_approved
                                if review_status == Project.ReviewStatus.APPROVED
                                else (
                                    project_comments_revision
                                    if review_status == Project.ReviewStatus.NEEDS_REVISION
                                    else project_comments_rejected
                                )
                            ),
                        )

                projects.append(project)

            self.stdout.write(self.style.SUCCESS('Projects created.'))

            # -----------------------------------
            # Applications
            # -----------------------------------

            applications_count = 0

            simple_public_projects = [
                project
                for project in projects
                if (
                    project.project_mode == Project.ProjectMode.SIMPLE
                    and project.review_status == Project.ReviewStatus.APPROVED
                    and project.status == Project.Status.ACTIVE
                )
            ]

            for project in simple_public_projects:
                applicant_pool = [
                    user
                    for user in users
                    if user.id != project.creator_id
                    and not (
                        project.company
                        and project.company.owner_id == user.id
                    )
                ]

                if not applicant_pool:
                    continue

                applicants = random.sample(
                    applicant_pool,
                    random.randint(1, min(5, len(applicant_pool))),
                )

                for applicant in applicants:
                    proposed_price = random.randint(
                        max(500_000, int(project.budget_min * 0.75)),
                        int(project.budget_max * 1.15),
                    )

                    Application.objects.create(
                        project=project,
                        applicant=applicant,
                        cover_letter=fake.text(max_nb_chars=300),
                        proposed_price=proposed_price,
                        status=random.choice([
                            Application.Status.PENDING,
                            Application.Status.ACCEPTED,
                            Application.Status.REJECTED,
                        ]),
                    )
                    applications_count += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f'{applications_count} applications created.'
                )
            )

            # -----------------------------------
            # Bids
            # -----------------------------------

            bids_count = 0

            tender_public_projects = [
                project
                for project in projects
                if (
                    project.project_mode == Project.ProjectMode.TENDER
                    and project.review_status == Project.ReviewStatus.APPROVED
                    and project.status in [
                        Project.Status.ACTIVE,
                        Project.Status.CLOSED,
                    ]
                )
            ]

            for project in tender_public_projects:
                bidder_pool = [
                    user
                    for user in users
                    if user.id != project.creator_id
                    and not (
                        project.company
                        and project.company.owner_id == user.id
                    )
                ]

                if not bidder_pool:
                    continue

                bidders = random.sample(
                    bidder_pool,
                    random.randint(2, min(5, len(bidder_pool))),
                )

                make_closed = random.random() < 0.35

                if make_closed and len(bidders) >= 2:
                    winner = random.choice(bidders)

                    for bidder in bidders:
                        accepted = bidder.id == winner.id
                        Bid.objects.create(
                            project=project,
                            freelancer=bidder,
                            amount=random.randint(
                                max(1_000_000, int(project.budget_min * 0.8)),
                                int(project.budget_max * 1.05),
                            ),
                            delivery_days=random.randint(7, 60),
                            cover_letter=fake.text(max_nb_chars=350),
                            status=(
                                Bid.Status.ACCEPTED
                                if accepted
                                else Bid.Status.REJECTED
                            ),
                            accepted_at=timezone.now() if accepted else None,
                        )
                        bids_count += 1

                    project.status = Project.Status.CLOSED
                    project.save(update_fields=['status'])
                else:
                    for bidder in bidders:
                        Bid.objects.create(
                            project=project,
                            freelancer=bidder,
                            amount=random.randint(
                                max(1_000_000, int(project.budget_min * 0.85)),
                                int(project.budget_max * 1.05),
                            ),
                            delivery_days=random.randint(7, 60),
                            cover_letter=fake.text(max_nb_chars=350),
                            status=Bid.Status.PENDING,
                        )
                        bids_count += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f'{bids_count} bids created.'
                )
            )

            # -----------------------------------
            # Favorites
            # -----------------------------------

            favorites_count = 0

            public_projects = [
                project
                for project in projects
                if (
                    project.status == Project.Status.ACTIVE
                    and project.review_status == Project.ReviewStatus.APPROVED
                )
            ]

            for user in users:
                if not public_projects:
                    break

                fav_count = random.randint(
                    2,
                    min(8, len(public_projects)),
                )

                fav_projects = random.sample(
                    public_projects,
                    fav_count,
                )

                for project in fav_projects:
                    if project.creator_id == user.id:
                        continue

                    if (
                        project.company
                        and project.company.owner_id == user.id
                    ):
                        continue

                    obj, created = Favorite.objects.get_or_create(
                        user=user,
                        project=project,
                    )
                    if created:
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