import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

from ....accounts.models import User
from ....categories.models import Category
from ....skills.models import Skill
from ....companies.models import Company
from ....projects.models import Project
from ....applications.models import Application
from ....bids.models import Bid
from ....favorites.models import Favorite
from ....projects.models import Milestone
from ....resumes.models import Resume, ResumeExperience


def make_slug(value):
    return slugify(value, allow_unicode=True)


# --- curated Persian data (kept short + realistic on purpose) ---

FIRST_NAMES_MALE = [
    'علی', 'رضا', 'محمد', 'حسین', 'امیر', 'مهدی',
    'سعید', 'مجید', 'کاوه', 'آرش', 'پارسا', 'سینا',
]

FIRST_NAMES_FEMALE = [
    'زهرا', 'فاطمه', 'مریم', 'نگار', 'سارا', 'الهام',
    'پریسا', 'مینا', 'لیلا', 'نازنین', 'هستی', 'ندا',
]

LAST_NAMES = [
    'احمدی', 'محمدی', 'رضایی', 'حسینی', 'کریمی', 'موسوی',
    'جعفری', 'صادقی', 'کاظمی', 'رحیمی', 'نوری', 'اکبری',
    'قاسمی', 'شریفی', 'یوسفی', 'هاشمی',
]

CITIES = [
    'تهران', 'مشهد', 'اصفهان', 'شیراز', 'تبریز', 'کرج',
    'اهواز', 'قم', 'رشت', 'یزد', 'کرمان', 'ارومیه',
]

COMPANY_NAMES = [
    'فناوری داده‌پرداز', 'گروه نرم‌افزاری آسا', 'پویا سیستم',
    'رایان‌تک', 'هوشمندگستر', 'داده‌کاوان', 'وب‌آفرین',
    'نوآوران دیجیتال', 'پارس‌کد', 'ابری‌سازان',
]

PROJECT_TITLES = [
    'طراحی سایت فروشگاهی',
    'اپلیکیشن موبایل فروشگاه',
    'ربات تلگرام هوشمند',
    'داشبورد مدیریت فروش',
    'طراحی لوگو حرفه‌ای',
    'سایت شرکتی وردپرس',
    'اپ اندروید سفارش غذا',
    'طراحی API فروشگاه',
    'طراحی رابط کاربری اپ',
    'بهینه‌سازی سئو سایت',
    'تحلیل داده فروش',
    'اپلیکیشن رزرو نوبت',
    'میکروسرویس پرداخت',
    'چت‌بات پشتیبانی',
    'دیتا اسکرپینگ سایت',
    'سیستم CRM شرکتی',
    'درگاه پرداخت آنلاین',
    'پنل ادمین جنگو',
    'اپ فروشگاهی iOS',
    'داشبورد تحلیلی',
    'سایت آموزش آنلاین',
    'طراحی لندینگ پیج',
    'ربات معامله‌گر ارز',
    'اپ مدیریت تسک',
]

DESCRIPTIONS = [
    'به یک توسعه‌دهنده باتجربه برای انجام این پروژه نیاز داریم. '
    'لطفاً نمونه‌کارهای مرتبط خود را همراه با پیشنهاد ارسال کنید.',

    'این پروژه شامل طراحی، پیاده‌سازی و تحویل نهایی است. '
    'کیفیت کد و تحویل به‌موقع برای ما اهمیت زیادی دارد.',

    'به دنبال فردی هستیم که بتواند به‌صورت مستقل کار کند و '
    'گزارش پیشرفت را به‌صورت هفتگی ارائه دهد.',

    'جزئیات کامل پروژه پس از انتخاب فریلنسر ارسال می‌شود. '
    'آشنایی با تکنولوژی‌های به‌روز الزامی است.',

    'یک پروژه‌ی کوتاه‌مدت با امکان همکاری بلندمدت. '
    'ارتباط خوب و تعهد به زمان‌بندی برای ما مهم است.',
]

HEADLINES = [
    'توسعه‌دهنده فرانت‌اند',
    'توسعه‌دهنده بک‌اند',
    'برنامه‌نویس فول‌استک',
    'طراح رابط کاربری',
    'متخصص علم داده',
    'توسعه‌دهنده موبایل',
]

ABOUT_TEXTS = [
    'چند سال است در حوزه نرم‌افزار فعالیت می‌کنم و به کیفیت کد '
    'و تحویل به‌موقع اهمیت می‌دهم.',

    'علاقه‌مند به یادگیری تکنولوژی‌های جدید و کار تیمی هستم و '
    'تجربه همکاری با تیم‌های مختلف را دارم.',

    'تمرکز من روی ساخت محصول‌های قابل‌اعتماد و ساده برای کاربر است.',
]

EXPERIENCE_TITLES = [
    'توسعه‌دهنده نرم‌افزار',
    'برنامه‌نویس وب',
    'کارشناس فنی',
    'طراح محصول',
]

MILESTONE_TITLES = [
    'تحلیل و طراحی اولیه',
    'پیاده‌سازی نسخه اول',
    'رفع بازخوردها',
    'تحویل نهایی و مستندات',
]

COVER_LETTERS = [
    'سلام، من تجربه‌ی مرتبط با این پروژه را دارم و می‌توانم '
    'در زمان مقرر آن را تحویل دهم.',

    'با سلام، نمونه‌کارهای مشابهی انجام داده‌ام و آماده‌ی '
    'شروع همکاری هستم.',

    'درود، پیشنهاد من شامل تحلیل، پیاده‌سازی و پشتیبانی '
    'اولیه پس از تحویل است.',

    'سلام، مهارت‌های لازم برای این کار را دارم و می‌توانم '
    'کیفیت مطلوب را تضمین کنم.',
]


class Command(BaseCommand):

    help = 'Seed fake data (Persian, realistic)'

    def handle(self, *args, **kwargs):

        self.stdout.write(
            self.style.WARNING('Deleting old data...')
        )

        ResumeExperience.objects.all().delete()
        Resume.objects.all().delete()
        Milestone.objects.all().delete()
        Favorite.objects.all().delete()
        Bid.objects.all().delete()
        Application.objects.all().delete()
        Project.objects.all().delete()
        Company.objects.all().delete()
        Skill.objects.all().delete()
        Category.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        self.stdout.write(
            self.style.SUCCESS('Old data deleted.')
        )

        # -----------------------------------
        # Categories
        # -----------------------------------

        category_data = [
            {'name': 'هوش مصنوعی', 'icon': 'fa-solid fa-robot'},
            {'name': 'طراحی وب', 'icon': 'fa-solid fa-globe'},
            {'name': 'بک‌اند', 'icon': 'fa-solid fa-server'},
            {'name': 'فرانت‌اند', 'icon': 'fa-solid fa-code'},
            {'name': 'اپلیکیشن موبایل', 'icon': 'fa-solid fa-mobile-screen'},
            {'name': 'DevOps و زیرساخت', 'icon': 'fa-solid fa-cloud'},
            {'name': 'رابط کاربری', 'icon': 'fa-solid fa-palette'},
            {'name': 'علم داده', 'icon': 'fa-solid fa-chart-line'},
        ]

        categories = []

        for item in category_data:

            category = Category.objects.create(
                name=item['name'],
                slug=make_slug(item['name']),
                icon=item['icon'],
            )

            categories.append(category)

        self.stdout.write(
            self.style.SUCCESS('Categories created.')
        )

        # -----------------------------------
        # Skills
        # -----------------------------------

        skill_names = [
            'Python', 'Django', 'FastAPI', 'React', 'Vue',
            'Docker', 'Kubernetes', 'TensorFlow', 'PyTorch',
            'Linux', 'Redis', 'Celery', 'SQL Server',
            'PostgreSQL', 'JavaScript', 'TypeScript', 'SASS',
            'Tailwind',
        ]

        skills = []

        for name in skill_names:

            skill = Skill.objects.create(
                name=name,
                slug=name.lower().replace(' ', '-'),
            )

            skills.append(skill)

        self.stdout.write(
            self.style.SUCCESS('Skills created.')
        )

        # -----------------------------------
        # Users
        # -----------------------------------

        users = []

        for i in range(20):

            if random.choice([True, False]):
                gender = User.Gender.MALE
                first_name = random.choice(FIRST_NAMES_MALE)
            else:
                gender = User.Gender.FEMALE
                first_name = random.choice(FIRST_NAMES_FEMALE)

            last_name = random.choice(LAST_NAMES)

            user = User.objects.create_user(
                email=f'user{i}@test.com',
                first_name=first_name,
                last_name=last_name,
                gender=gender,
                phone=f'09{random.randint(100000000, 999999999)}',
                password='Test12345',
            )

            users.append(user)

        # two experts covering all categories
        experts = random.sample(users, 2)

        for expert in experts:

            expert.is_expert = True

            expert.save(
                update_fields=['is_expert'],
            )

            expert.expert_categories.set(categories)

        self.stdout.write(
            self.style.SUCCESS('Users created (2 experts).')
        )

        # -----------------------------------
        # Companies
        # -----------------------------------

        companies = []

        company_users = random.sample(users, 8)

        company_names = random.sample(
            COMPANY_NAMES,
            len(company_users),
        )

        for user, name in zip(company_users, company_names):

            company = Company.objects.create(
                owner=user,
                name=name,
                description=random.choice(DESCRIPTIONS),
                phone=f'09{random.randint(100000000, 999999999)}',
                address=f'{random.choice(CITIES)}، خیابان اصلی',
                is_verified=random.choice([True, False]),
            )

            companies.append(company)

        self.stdout.write(
            self.style.SUCCESS('Companies created.')
        )

        # -----------------------------------
        # Projects
        # -----------------------------------

        simple_projects = []
        tender_projects = []

        for i in range(50):

            creator = random.choice(users)

            user_company = getattr(creator, 'company', None)

            use_company = (
                user_company is not None
                and random.choice([True, False])
            )

            primary_category = random.choice(categories)

            extra_categories = random.sample(
                categories,
                random.randint(1, 3),
            )

            # tender ~ 40% of projects
            project_mode = random.choice([
                Project.ProjectMode.SIMPLE,
                Project.ProjectMode.SIMPLE,
                Project.ProjectMode.SIMPLE,
                Project.ProjectMode.TENDER,
                Project.ProjectMode.TENDER,
            ])

            budget_min = random.randint(1, 10) * 500000
            budget_max = budget_min + random.randint(2, 60) * 500000

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

                title=random.choice(PROJECT_TITLES),

                description=random.choice(DESCRIPTIONS),

                budget_min=budget_min,
                budget_max=budget_max,

                location=random.choice(CITIES),

                deadline=(
                    timezone.now().date()
                    + timedelta(days=random.randint(3, 30))
                ),

                project_mode=project_mode,

                skill_level=random.choice([
                    Project.SkillLevel.NONE,
                    Project.SkillLevel.BEGINNER,
                    Project.SkillLevel.BEGINNER,
                    Project.SkillLevel.INTERMEDIATE,
                    Project.SkillLevel.INTERMEDIATE,
                    Project.SkillLevel.EXPERT,
                ]),

                # most projects visible in listings
                status=Project.Status.ACTIVE,
                review_status=Project.ReviewStatus.APPROVED,
                reviewed_at=timezone.now(),
            )

            project.categories.set(
                list(set(extra_categories + [primary_category]))
            )

            selected_skills = random.sample(
                skills,
                random.randint(2, 6),
            )

            project.skills.set(selected_skills)

            if project_mode == Project.ProjectMode.TENDER:
                tender_projects.append(project)
            else:
                simple_projects.append(project)

        self.stdout.write(
            self.style.SUCCESS(
                f'{len(simple_projects)} simple + '
                f'{len(tender_projects)} tender projects created.'
            )
        )

        # -----------------------------------
        # Applications (for SIMPLE projects)
        # -----------------------------------

        applications_count = 0

        for project in simple_projects:

            applicants = random.sample(
                users,
                random.randint(1, 5),
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
                    applicant=applicant,
                ).exists()

                if exists:
                    continue

                Application.objects.create(
                    project=project,
                    applicant=applicant,
                    cover_letter=random.choice(COVER_LETTERS),
                    proposed_price=(
                        random.randint(1, 20) * 500000
                    ),
                    status=random.choice([
                        Application.Status.PENDING,
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
        # Bids (for TENDER projects)
        # -----------------------------------

        bids_count = 0

        for project in tender_projects:

            bidders = random.sample(
                users,
                random.randint(1, 5),
            )

            for bidder in bidders:

                if bidder.id == project.creator_id:
                    continue

                if (
                    project.company
                    and project.company.owner_id == bidder.id
                ):
                    continue

                exists = Bid.objects.filter(
                    project=project,
                    freelancer=bidder,
                ).exists()

                if exists:
                    continue

                bid = Bid.objects.create(
                    project=project,
                    freelancer=bidder,
                    amount=random.randint(1, 20) * 500000,
                    delivery_days=random.randint(3, 30),
                    cover_letter=random.choice(COVER_LETTERS),
                    status=random.choice([
                        Bid.Status.PENDING,
                        Bid.Status.PENDING,
                        Bid.Status.SHORTLISTED,
                        Bid.Status.REJECTED,
                    ]),
                )

                # ~70% of bids already scored by an expert
                expert = random.choice(experts)

                can_score = (
                    expert.id != bid.freelancer_id
                    and expert.id != project.creator_id
                )

                if can_score and random.random() < 0.7:

                    price_score = random.randint(1, 5)
                    experience_score = random.randint(1, 5)

                    bid.price_score = price_score
                    bid.experience_score = experience_score
                    bid.expert_score = (
                        (price_score + experience_score) / 2
                    )
                    bid.score_note = (
                        'قیمت نسبت به بودجه و سابقه فریلنسر '
                        'بررسی شد.'
                    )
                    bid.scored_by = expert
                    bid.scored_at = timezone.now()

                    bid.save(
                        update_fields=[
                            'price_score',
                            'experience_score',
                            'expert_score',
                            'score_note',
                            'scored_by',
                            'scored_at',
                        ]
                    )

                # ~25% get a one-time employer message
                if random.random() < 0.25:

                    bid.employer_message = (
                        'سلام، امکانش هست قیمت یا زمان تحویل '
                        'را کمی بهتر کنید؟'
                    )

                    bid.employer_message_at = timezone.now()

                    bid.save(
                        update_fields=[
                            'employer_message',
                            'employer_message_at',
                        ]
                    )

                bids_count += 1

        # winners on roughly a third of tender projects
        winners_count = 0

        for project in tender_projects:

            if random.random() > 0.35:
                continue

            project_bids = list(
                Bid.objects.filter(project=project)
            )

            if not project_bids:
                continue

            winner = random.choice(project_bids)

            winner.status = Bid.Status.ACCEPTED
            winner.accepted_at = timezone.now()

            winner.save(
                update_fields=['status', 'accepted_at'],
            )

            Bid.objects.filter(
                project=project,
            ).exclude(
                pk=winner.pk,
            ).update(
                status=Bid.Status.REJECTED,
            )

            project.status = Project.Status.CLOSED

            project.save(
                update_fields=['status'],
            )

            winners_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'{bids_count} bids created, '
                f'{winners_count} winners picked.'
            )
        )

        # -----------------------------------
        # Favorites
        # -----------------------------------

        all_projects = simple_projects + tender_projects

        favorites_count = 0

        for user in users:

            fav_projects = random.sample(
                all_projects,
                random.randint(2, 8),
            )

            for project in fav_projects:

                exists = Favorite.objects.filter(
                    user=user,
                    project=project,
                ).exists()

                if exists:
                    continue

                Favorite.objects.create(
                    user=user,
                    project=project,
                )

                favorites_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'{favorites_count} favorites created.'
            )
        )

        # -----------------------------------
        # Resumes
        # -----------------------------------

        resumes_count = 0

        resume_users = random.sample(users, 12)

        for user in resume_users:

            resume = Resume.objects.create(
                user=user,
                headline=random.choice(HEADLINES),
                about=random.choice(ABOUT_TEXTS),
                city=random.choice(CITIES),
                is_public=random.choice(
                    [True, True, True, False]
                ),
            )

            resume.skills.set(
                random.sample(
                    skills,
                    random.randint(3, 6),
                )
            )

            for i in range(random.randint(1, 2)):

                start = timezone.now().date() - timedelta(
                    days=random.randint(400, 2000),
                )

                still_working = random.choice(
                    [True, False]
                )

                ResumeExperience.objects.create(
                    resume=resume,
                    title=random.choice(EXPERIENCE_TITLES),
                    company=random.choice(COMPANY_NAMES),
                    description=random.choice(DESCRIPTIONS),
                    start_date=start,
                    end_date=(
                        None
                        if still_working
                        else start + timedelta(
                            days=random.randint(180, 700),
                        )
                    ),
                )

            resumes_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'{resumes_count} resumes created.'
            )
        )

        # -----------------------------------
        # Milestones (projects with winners)
        # -----------------------------------

        milestones_count = 0

        won_projects = Project.objects.filter(
            bids__status=Bid.Status.ACCEPTED,
        ).distinct()

        for project in won_projects:

            titles = random.sample(
                MILESTONE_TITLES,
                random.randint(2, 4),
            )

            statuses = []

            for i, title in enumerate(titles):

                if i == 0:
                    milestone_status = Milestone.Status.APPROVED
                elif i == 1:
                    milestone_status = random.choice([
                        Milestone.Status.APPROVED,
                        Milestone.Status.DELIVERED,
                    ])
                else:
                    milestone_status = Milestone.Status.PENDING

                statuses.append(milestone_status)

                Milestone.objects.create(
                    project=project,
                    title=title,
                    description=random.choice(DESCRIPTIONS),
                    due_date=(
                        timezone.now().date()
                        + timedelta(days=(i + 1) * 7)
                    ),
                    status=milestone_status,
                    delivered_at=(
                        timezone.now()
                        if milestone_status
                        != Milestone.Status.PENDING
                        else None
                    ),
                    approved_at=(
                        timezone.now()
                        if milestone_status
                        == Milestone.Status.APPROVED
                        else None
                    ),
                )

                milestones_count += 1

            all_approved = True

            for milestone_status in statuses:

                if milestone_status != Milestone.Status.APPROVED:
                    all_approved = False

            if all_approved:

                project.status = Project.Status.COMPLETED

                project.save(
                    update_fields=['status'],
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'{milestones_count} milestones created.'
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                'FAKE DATA CREATED SUCCESSFULLY'
            )
        )
