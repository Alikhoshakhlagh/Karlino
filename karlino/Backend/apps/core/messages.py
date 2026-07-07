# General
PERMISSION_DENIED = (
    'شما دسترسی لازم برای انجام این عملیات را ندارید.'
)

NOT_FOUND = (
    'مورد درخواستی یافت نشد.'
)

INVALID_REQUEST = (
    'درخواست ارسالی معتبر نیست.'
)

# Authentication
INVALID_CREDENTIALS = (
    'ایمیل یا رمز عبور اشتباه است.'
)

LOGIN_REQUIRED = (
    'برای انجام این عملیات ابتدا وارد حساب کاربری خود شوید.'
)

PASSWORD_NOT_MATCH = (
    'پسورد یکسان نیست.'
)

EMAIL_REQUIRED = (
    'وارد کردن ایمیل الزامی است.'
)

FIRST_NAME_REQUIRED = (
    'وارد کردن نام الزامی است.'
)

LAST_NAME_REQUIRED = (
    'وارد کردن نام خانوادگی الزامی است.'
)

# Projects
PROJECT_NOT_ACTIVE = (
    'این پروژه فعال نیست.'
)

PROJECT_NOT_APPROVED = (
    'این پروژه هنوز تایید نشده است.'
)

PROJECT_ALREADY_REVIEWED = (
    'این پروژه قبلاً بررسی شده است.'
)

PROJECT_NOT_TENDER = (
    'این پروژه از نوع مناقصه‌ای نیست.'
)

OWN_PROJECT_BID_REVIEWED = (
    'شما نمی‌توانید روی پروژه خودتان پیشنهاد ثبت کنید.'
)

OWN_COMPANY_BID_REVIEWED = (
    'شما نمی‌توانید روی پروژه شرکت خودتان پیشنهاد ثبت کنید.'
)

PROJECT_SUBMITTED_FOR_REVIEW = (
    'پروژه با موفقیت برای بررسی ارسال شد.'
)

PROJECT_NOT_NEEDS_REVISION = (
    'فقط پروژه‌هایی که نیاز به اصلاح دارند قابل ارسال مجدد هستند.'
)

#Apply
ALREADY_APPLIED = (
    'شما قبلا برای این پروژه درخواست داده اید.'
)

PROJECT_REQUIRED = (
    'شما پروژه ای انتخاب نکرده اید.'
)

# Expert
EXPERT_CATEGORY_DENIED = (
    'شما اجازه بررسی این دسته‌بندی را ندارید.'
)

SELF_REVIEW_FORBIDDEN = (
    'شما نمی‌توانید پروژه خودتان را بررسی کنید.'
)

REVIEW_SUBMITTED = (
    'بررسی پروژه با موفقیت ثبت شد.'
)

# Bid
BID_ACCEPTED = (
    'پیشنهاد با موفقیت پذیرفته شد.'
)

BID_ALREADY_EXISTS = (
    'برای این پروژه قبلاً پیشنهاد ثبت کرده‌اید.'
)

# Company
COMPANY_REQUIRED = (
    'ابتدا باید پروفایل شرکت خود را تکمیل کنید.'
)

COMPANY_NOT_OWNED = (
    'فقط می‌توانید از شرکت متعلق به خودتان استفاده کنید.'
)

COMPANY_ON_PERSONAL = (
    'پروژه شخصی نمیتواند شرکت داشته باشد.'
)

COMPANY_EXISTS = (
    'شما قبلاً یک شرکت ثبت کرده‌اید.'
)

# Validation
DEADLINE_IN_PAST = (
    'مهلت انجام پروژه نمی‌تواند قبل از امروز باشد.'
)

INVALID_BUDGET_RANGE = (
    'حداقل بودجه نمی‌تواند بیشتر از حداکثر بودجه باشد.'
)

MIN_BUDGET_TOO_LOW = (
    'حداقل بودجه نمی‌تواند کمتر از 100 هزار تومان باشد.'
)

MAX_BUDGET_TOO_HIGH = (
    'حداکثر بودجه نامعتبر است.'
)

COMMENT_REQUIRED = (
    'وارد کردن توضیحات الزامی است.'
)

#Slug
INVALID_SLUG = (
    'اسلاگ فقط می‌تواند شامل حروف انگلیسی کوچک، اعداد و خط تیره (-) باشد.'
)

# Account / Sessions
OLD_PASSWORD_INCORRECT = (
    'رمز عبور فعلی اشتباه است.'
)

PASSWORD_CHANGED = (
    'رمز عبور با موفقیت تغییر کرد.'
)

SESSION_NOT_FOUND = (
    'نشست موردنظر یافت نشد.'
)

SESSION_REVOKED = (
    'نشست موردنظر با موفقیت خارج شد.'
)

# Password / Account
USER_NOT_FOUND = (
    'کاربری با این ایمیل یافت نشد.'
)

PASSWORD_RESET_SUCCESS = (
    'رمز عبور با موفقیت بازنشانی شد.'
)

PASSWORD_TOO_SHORT = (
    'رمز عبور باید حداقل ۸ کاراکتر باشد.'
)

# Bid validation
BID_AMOUNT_INVALID = (
    'مبلغ پیشنهاد معتبر نیست.'
)

BID_DELIVERY_INVALID = (
    'مدت تحویل باید حداقل ۱ روز باشد.'
)

COVER_LETTER_REQUIRED = (
    'وارد کردن متن پیشنهاد الزامی است.'
)

BID_LOCKED = (
    'این پیشنهاد دیگر قابل ویرایش نیست.'
)

# Bid scoring (expert)
BID_SCORE_SUBMITTED = (
    'امتیاز پیشنهاد با موفقیت ثبت شد.'
)

BID_ALREADY_SCORED = (
    'این پیشنهاد قبلاً امتیازدهی شده است.'
)

BID_SCORE_INVALID = (
    'امتیاز باید عددی بین ۱ تا ۵ باشد.'
)

SELF_SCORE_FORBIDDEN = (
    'شما نمی‌توانید به پیشنهادهای مرتبط با خودتان امتیاز بدهید.'
)

# Employer message on bid
EMPLOYER_MESSAGE_SENT = (
    'پیام شما برای فریلنسر ارسال شد.'
)

EMPLOYER_MESSAGE_ALREADY_SENT = (
    'شما قبلاً برای این پیشنهاد پیام ارسال کرده‌اید.'
)

EMPLOYER_MESSAGE_EMPTY = (
    'متن پیام نمی‌تواند خالی باشد.'
)

BID_NOT_OPEN = (
    'این پیشنهاد در وضعیتی نیست که بتوان برای آن پیام ارسال کرد.'
)

PRICE_SCORE_INVALID = (
    'امتیاز قیمت باید عددی بین ۱ تا ۵ باشد.'
)

PRICE_BELOW_BUDGET = (
    'قیمت پیشنهادی نمی‌تواند کمتر از حداقل بودجه پروژه باشد.'
)

PRICE_ABOVE_BUDGET = (
    'قیمت پیشنهادی نمی‌تواند بیشتر از حداکثر بودجه پروژه باشد.'
)

EXPERIENCE_SCORE_INVALID = (
    'امتیاز سابقه باید عددی بین ۱ تا ۵ باشد.'
)

# Milestones
MILESTONE_NO_WINNER = (
    'برای این پروژه هنوز برنده‌ای انتخاب نشده است.'
)

MILESTONE_LOCKED = (
    'این مرحله دیگر قابل ویرایش نیست.'
)

MILESTONE_NOT_PENDING = (
    'این مرحله در وضعیت قابل تحویل نیست.'
)

MILESTONE_NOT_DELIVERED = (
    'این مرحله هنوز تحویل داده نشده است.'
)

MILESTONE_DELIVERED = (
    'مرحله با موفقیت تحویل داده شد.'
)

MILESTONE_APPROVED = (
    'مرحله تأیید شد.'
)

MILESTONE_REJECTED = (
    'مرحله برای اصلاح به فریلنسر بازگردانده شد.'
)

PROJECT_COMPLETED = (
    'همه مراحل تأیید شد و پروژه تکمیل گردید.'
)

# Resume
RESUME_EXISTS = (
    'شما قبلاً رزومه ساخته‌اید.'
)

RESUME_NOT_FOUND = (
    'رزومه‌ای برای این کاربر یافت نشد.'
)

RESUME_PRIVATE = (
    'رزومه این کاربر خصوصی است.'
)

EXPERIENCE_NOT_FOUND = (
    'سابقه کاری موردنظر یافت نشد.'
)

# Application (accept / reject)
APPLICATION_NOT_PENDING = (
    'این درخواست در وضعیت «در انتظار» نیست و قابل تغییر نیست.'
)

APPLICATION_ACCEPTED = (
    'درخواست با موفقیت تأیید شد.'
)

APPLICATION_REJECTED = (
    'درخواست رد شد.'
)