// ===== محافظ ورود: اگر کاربر لاگین نیست، به صفحه‌ی ورود برود =====
if (!localStorage.getItem("access")) {
    window.location.href = "login.html";
}

// ===== المنت‌ها =====
const navItems = document.querySelectorAll(".sidebar-nav .nav-item");
const sections = document.querySelectorAll(".dashboard-section");

const sidebarUserName = document.getElementById("sidebarUserName");
const sidebarUserEmail = document.getElementById("sidebarUserEmail");

const summaryCards = document.getElementById("summaryCards");
const summaryChartBox = document.getElementById("summaryChartBox");
const myProjectsList = document.getElementById("myProjectsList");
const myApplicationsList = document.getElementById("myApplicationsList");
const favoritesList = document.getElementById("favoritesList");
const incomingApplicationsList = document.getElementById("incomingApplicationsList");
const incomingActionsError = document.getElementById("error-incoming-actions");
const sessionsList = document.getElementById("sessionsList");

// یادمان می‌ماند کدام بخش‌ها قبلاً لود شده‌اند تا دوباره درخواست نزنیم
const loadedSections = {};

// ===== توابع کمکی =====

// جلوگیری از XSS: داده‌ای که از سرور می‌آید را قبل از گذاشتن در HTML امن می‌کنیم
function escapeHtml(text) {
    if (text === null || text === undefined) {
        return "";
    }
    const div = document.createElement("div");
    div.textContent = String(text);
    return div.innerHTML;
}

// تاریخ را به شمسی نشان می‌دهد
function formatDate(dateString) {
    if (!dateString) {
        return "—";
    }
    const date = new Date(dateString);
    return date.toLocaleDateString("fa-IR");
}

// عدد را با جداکننده‌ی فارسی نشان می‌دهد
function formatNumber(value) {
    if (value === null || value === undefined || value === "") {
        return "—";
    }
    return Number(value).toLocaleString("fa-IR");
}

// وضعیت پروژه به فارسی
function projectStatusFa(status) {
    if (status === "draft") return "پیش‌نویس";
    if (status === "active") return "فعال";
    if (status === "closed") return "بسته‌شده";
    if (status === "completed") return "تکمیل‌شده";
    if (status === "archived") return "بایگانی‌شده";
    return status;
}

// وضعیت درخواست به فارسی
function bidStatusFa(status) {
    if (status === "pending") return "در انتظار";
    if (status === "shortlisted") return "منتخب اولیه";
    if (status === "accepted") return "پذیرفته‌شده";
    if (status === "rejected") return "ردشده";
    if (status === "withdrawn") return "انصراف‌داده‌شده";
    return status;
}

// کلاس رنگ نشان وضعیت
function statusClass(status) {
    if (status === "accepted" || status === "active" || status === "completed") return "success";
    if (status === "pending" || status === "draft") return "warning";
    if (status === "rejected" || status === "archived") return "danger";
    if (status === "shortlisted") return "info";
    return "";
}

// تشخیص خطای ۴۰۴ (یعنی این endpoint هنوز روی سرور فعال نشده)
function isNotFound(error) {
    return error && String(error.message).indexOf("404") !== -1;
}

// پاسخ سرور ممکن است آرایه باشد یا صفحه‌بندی‌شده (results)
function getItems(data) {
    if (Array.isArray(data)) {
        return data;
    }
    if (data && Array.isArray(data.results)) {
        return data.results;
    }
    return [];
}

// پاک‌کردن همه‌ی خطاها و پیام موفقیت یک فرم
function clearFormMessages(form) {
    const errors = form.querySelectorAll(".field-error");
    errors.forEach(function (error) {
        error.textContent = "";
        error.classList.remove("show");
    });

    const success = form.querySelector(".form-success");
    if (success) {
        success.textContent = "";
        success.classList.remove("show");
    }
}

// نشان‌دادن خطای یک فیلد
function showFieldError(id, message) {
    const element = document.getElementById(id);
    if (element) {
        element.textContent = message;
        element.classList.add("show");
    }
}

// خلاصه‌کردن اسم دستگاه از روی user agent
// مثلاً: "Chrome - ویندوز" به‌جای رشته‌ی طولانی user agent
function shortDeviceName(userAgent) {
    if (!userAgent) {
        return "دستگاه ناشناخته";
    }

    // تشخیص مرورگر (ترتیب مهم است، چون Edge و Opera هم کلمه‌ی Chrome را دارند)
    let browser = "مرورگر ناشناخته";
    if (userAgent.indexOf("Edg") !== -1) {
        browser = "Edge";
    } else if (userAgent.indexOf("OPR") !== -1 || userAgent.indexOf("Opera") !== -1) {
        browser = "Opera";
    } else if (userAgent.indexOf("Chrome") !== -1) {
        browser = "Chrome";
    } else if (userAgent.indexOf("Firefox") !== -1) {
        browser = "Firefox";
    } else if (userAgent.indexOf("Safari") !== -1) {
        browser = "Safari";
    }

    // تشخیص سیستم‌عامل
    let os = "";
    if (userAgent.indexOf("Windows") !== -1) {
        os = "ویندوز";
    } else if (userAgent.indexOf("Android") !== -1) {
        os = "اندروید";
    } else if (userAgent.indexOf("iPhone") !== -1 || userAgent.indexOf("iPad") !== -1) {
        os = "آیفون / آیپد";
    } else if (userAgent.indexOf("Mac") !== -1) {
        os = "مک";
    } else if (userAgent.indexOf("Linux") !== -1) {
        os = "لینوکس";
    }

    if (os === "") {
        return browser;
    }

    return browser + " - " + os;
}

// ===== جابه‌جایی بین بخش‌های پنل =====
navItems.forEach(function (item) {
    item.addEventListener("click", function () {

        // دکمه‌ی فعال قبلی را غیرفعال کن
        navItems.forEach(function (other) {
            other.classList.remove("active");
        });
        item.classList.add("active");

        // همه‌ی بخش‌ها را مخفی کن و فقط بخش انتخاب‌شده را نشان بده
        const targetId = item.dataset.section;

        sections.forEach(function (section) {
            if (section.id === targetId) {
                section.classList.remove("hidden");
            } else {
                section.classList.add("hidden");
            }
        });

        // داده‌ی آن بخش را (فقط بار اول) لود کن
        loadSection(targetId);
    });
});

// هر بخش، بار اولی که باز می‌شود داده‌اش را می‌گیرد
function loadSection(sectionId) {
    if (loadedSections[sectionId]) {
        return;
    }
    loadedSections[sectionId] = true;

    if (sectionId === "section-summary") loadSummary();
    if (sectionId === "section-my-projects") loadMyProjects();
    if (sectionId === "section-incoming-applications") loadIncomingApplications();
    if (sectionId === "section-my-applications") loadMyApplications();
    if (sectionId === "section-favorites") loadFavorites();
    if (sectionId === "section-profile") loadProfile();
    if (sectionId === "section-company") loadCompany();
    if (sectionId === "section-security") loadSessions();
}

// ===== خلاصه وضعیت =====
async function loadSummary() {
    summaryCards.innerHTML = "<p class='loading-text'>در حال بارگذاری...</p>";

    try {
        const data = await apiRequest(ENDPOINTS.dashboard);

        // برچسب و آیکون هر آمار
        const stats = [
            { key: "my_projects_count", label: "کل پروژه‌های من", icon: "fa-diagram-project" },
            { key: "active_projects_count", label: "پروژه‌های فعال", icon: "fa-bolt" },
            { key: "approved_projects_count", label: "پروژه‌های تأییدشده", icon: "fa-circle-check" },
            { key: "pending_projects_count", label: "در انتظار بررسی", icon: "fa-clock" },
            { key: "pending_review_projects_count", label: "در صف کارشناسی", icon: "fa-user-check" },
            { key: "needs_revision_projects_count", label: "نیازمند اصلاح", icon: "fa-rotate-left" },
            { key: "my_applications_count", label: "درخواست‌های من", icon: "fa-paper-plane" },
            { key: "my_bids_count", label: "پیشنهادهای من", icon: "fa-hand-holding-dollar" },
            { key: "favorites_count", label: "ذخیره‌شده‌ها", icon: "fa-bookmark" }
        ];

        let html = "";

        for (let i = 0; i < stats.length; i++) {
            const stat = stats[i];

            // اگر این آمار در پاسخ سرور نبود، کارتش را نساز
            if (data[stat.key] === undefined) {
                continue;
            }

            html += `
                <div class="stat-card">
                    <div class="stat-icon">
                        <i class="fa-solid ${stat.icon}"></i>
                    </div>
                    <p class="stat-value">${formatNumber(data[stat.key])}</p>
                    <p class="stat-label">${stat.label}</p>
                </div>
            `;
        }

        summaryCards.innerHTML = html;

    } catch (error) {
        if (isNotFound(error)) {
            summaryCards.innerHTML = "<p class='empty-text'>این بخش هنوز روی سرور فعال نشده است.</p>";
            return;
        }
        console.error("خطا در دریافت خلاصه وضعیت:", error);
        summaryCards.innerHTML = "<p class='field-error show'>خطا در دریافت اطلاعات داشبورد.</p>";
    }
}

// ===== نمودار فعالیت (داخل خلاصه وضعیت) =====
// از endpoint نمودارها فقط بخش «فعالیت ماهانه» را می‌گیریم
// و با کتابخانه‌ی Chart.js به صورت نمودار خطی نشان می‌دهیم.
async function loadActivityChart() {

    // اگر کتابخانه‌ی Chart.js لود نشده بود (مثلاً CDN در دسترس نبود)، نمودار را مخفی کن
    if (typeof Chart === "undefined") {
        summaryChartBox.classList.add("hidden");
        return;
    }

    try {
        const data = await apiRequest(ENDPOINTS.charts);
        const activity = data.monthly_activity;

        // اگر ساختار مورد انتظار (labels + datasets) را نداشت، نمودار را مخفی کن
        if (!activity || !Array.isArray(activity.labels) || !Array.isArray(activity.datasets)) {
            summaryChartBox.classList.add("hidden");
            return;
        }

        // برای هر خط نمودار یک رنگ از پالت سایت
        const lineColors = ["#fd653c", "#7f9fce", "#7fae95"];

        const datasets = [];

        for (let i = 0; i < activity.datasets.length; i++) {
            const item = activity.datasets[i];

            datasets.push({
                label: item.label,
                data: item.data,
                borderColor: lineColors[i % lineColors.length],
                backgroundColor: lineColors[i % lineColors.length],
                tension: 0.3,
                pointRadius: 3
            });
        }

        const canvas = document.getElementById("activityChart");

        new Chart(canvas, {
            type: "line",
            data: {
                labels: activity.labels,
                datasets: datasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        rtl: true,
                        labels: {
                            color: "#fdfdff",
                            font: { family: "Vazirmatn" }
                        }
                    }
                },
                scales: {
                    x: {
                        ticks: { color: "#a9b1c7", font: { family: "Vazirmatn" } },
                        grid: { color: "rgba(255, 255, 255, 0.06)" }
                    },
                    y: {
                        beginAtZero: true,
                        // precision: 0 یعنی روی محور فقط عدد صحیح نشان بده
                        ticks: { color: "#a9b1c7", precision: 0, font: { family: "Vazirmatn" } },
                        grid: { color: "rgba(255, 255, 255, 0.06)" }
                    }
                }
            }
        });

    } catch (error) {
        // اگر endpoint نمودارها روی سرور نبود یا خطا داد، فقط جعبه‌ی نمودار را مخفی می‌کنیم
        console.error("خطا در دریافت نمودار فعالیت:", error);
        summaryChartBox.classList.add("hidden");
    }
}

// ===== پروژه‌های من =====
async function loadMyProjects() {
    myProjectsList.innerHTML = "<p class='loading-text'>در حال بارگذاری...</p>";

    try {
        const data = await apiRequest(ENDPOINTS.myPosted);
        const projects = getItems(data);

        if (projects.length === 0) {
            myProjectsList.innerHTML = "<p class='empty-text'>هنوز پروژه‌ای ثبت نکرده‌اید.</p>";
            return;
        }

        let html = "";

        for (let i = 0; i < projects.length; i++) {
            const project = projects[i];

            html += `
                <div class="item-card">
                    <div class="item-top">
                        <p class="item-title">
                            <a href="project-detail.html?id=${escapeHtml(project.id)}">${escapeHtml(project.title)}</a>
                        </p>
                        <span class="status-badge ${statusClass(project.status)}">${projectStatusFa(project.status)}</span>
                    </div>
                    <div class="item-meta">
                        <span><i class="fa-solid fa-coins"></i> بودجه: ${escapeHtml(project.budget_display || "—")}</span>
                        <span><i class="fa-solid fa-paper-plane"></i> درخواست‌ها: ${formatNumber(project.applications_count || 0)}</span>
                        <span><i class="fa-solid fa-calendar"></i> ${formatDate(project.created_at)}</span>
                    </div>
                </div>
            `;
        }

        myProjectsList.innerHTML = html;

    } catch (error) {
        if (isNotFound(error)) {
            myProjectsList.innerHTML = "<p class='empty-text'>این بخش هنوز روی سرور فعال نشده است.</p>";
            return;
        }
        console.error("خطا در دریافت پروژه‌های من:", error);
        myProjectsList.innerHTML = "<p class='field-error show'>خطا در دریافت پروژه‌ها.</p>";
    }
}

// ===== درخواست‌های دریافتی =====
async function loadIncomingApplications() {
    incomingApplicationsList.innerHTML = "<p class='loading-text'>در حال بارگذاری...</p>";

    try {
        const data = await apiRequest(ENDPOINTS.incomingApplications);
        const applications = getItems(data);

        if (applications.length === 0) {
            incomingApplicationsList.innerHTML = "<p class='empty-text'>درخواستی برای پروژه‌های شما ثبت نشده است.</p>";
            return;
        }

        let html = "";

        for (let i = 0; i < applications.length; i++) {
            const app = applications[i];

            // اگر مدت زمان انجام ثبت شده باشد، آن را هم نشان بده
            let durationHtml = "";
            if (app.duration_days) {
                durationHtml = `<span><i class="fa-solid fa-clock"></i> مدت انجام: ${formatNumber(app.duration_days)} روز</span>`;
            }

            // عنوان پروژه اگر آیدی پروژه را داشتیم لینک می‌شود
            let titleHtml = escapeHtml(app.project_title);
            if (app.project) {
                titleHtml = `<a href="project-detail.html?id=${escapeHtml(app.project)}">${escapeHtml(app.project_title)}</a>`;
            }

            // دکمه‌های تأیید و رد فقط برای درخواست‌های «در انتظار»
            let actionsHtml = "";
            if (app.status === "pending") {
                actionsHtml = `
                    <div class="item-actions">
                        <button type="button" class="approve-btn" data-id="${escapeHtml(app.id)}">تأیید درخواست</button>
                        <button type="button" class="revoke-btn" data-id="${escapeHtml(app.id)}">رد درخواست</button>
                    </div>
                `;
            }

            html += `
                <div class="item-card">
                    <div class="item-top">
                        <p class="item-title">${titleHtml}</p>
                        <span class="status-badge ${statusClass(app.status)}">${bidStatusFa(app.status)}</span>
                    </div>
                    <div class="item-meta">
                        <span><i class="fa-solid fa-user"></i> متقاضی: ${escapeHtml(app.applicant_name)}</span>
                        <span><i class="fa-solid fa-coins"></i> قیمت پیشنهادی: ${formatNumber(app.proposed_price)}</span>
                        ${durationHtml}
                        <span><i class="fa-solid fa-calendar"></i> ${formatDate(app.created_at)}</span>
                    </div>
                    <div class="item-message">${escapeHtml(app.cover_letter)}</div>
                    ${actionsHtml}
                </div>
            `;
        }

        incomingApplicationsList.innerHTML = html;

        // به دکمه‌های «تأیید» گوش بده
        const approveButtons = incomingApplicationsList.querySelectorAll(".approve-btn");
        approveButtons.forEach(function (button) {
            button.addEventListener("click", function () {
                answerApplication(button.dataset.id, "accept");
            });
        });

        // به دکمه‌های «رد» گوش بده
        const rejectButtons = incomingApplicationsList.querySelectorAll(".revoke-btn");
        rejectButtons.forEach(function (button) {
            button.addEventListener("click", function () {
                answerApplication(button.dataset.id, "reject");
            });
        });

    } catch (error) {
        if (isNotFound(error)) {
            incomingApplicationsList.innerHTML = "<p class='empty-text'>این بخش هنوز روی سرور فعال نشده است.</p>";
            return;
        }
        console.error("خطا در دریافت درخواست‌های دریافتی:", error);
        incomingApplicationsList.innerHTML = "<p class='field-error show'>خطا در دریافت درخواست‌های دریافتی.</p>";
    }
}

// تأیید یا رد یک درخواست دریافتی
// action یا "accept" است یا "reject"
async function answerApplication(applicationId, action) {

    // پاک‌کردن خطای قبلی
    incomingActionsError.textContent = "";
    incomingActionsError.classList.remove("show");

    try {
        const response = await fetch(BASE_URL + ENDPOINTS.applications + applicationId + "/" + action + "/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + localStorage.getItem("access")
            }
        });

        const data = await response.json();

        if (response.ok) {
            // لیست را دوباره بگیر تا وضعیت جدید دیده شود
            loadIncomingApplications();
            return;
        }

        // پیام خطای فارسی سرور را نشان بده
        if (data.detail) {
            incomingActionsError.textContent = data.detail;
            incomingActionsError.classList.add("show");
        }

    } catch (error) {
        incomingActionsError.textContent = "ارتباط با سرور برقرار نشد";
        incomingActionsError.classList.add("show");
    }
}

// ===== درخواست‌های من =====
async function loadMyApplications() {
    myApplicationsList.innerHTML = "<p class='loading-text'>در حال بارگذاری...</p>";

    try {
        const data = await apiRequest(ENDPOINTS.myApplications);
        const applications = getItems(data);

        if (applications.length === 0) {
            myApplicationsList.innerHTML = "<p class='empty-text'>هنوز درخواستی نفرستاده‌اید.</p>";
            return;
        }

        let html = "";

        for (let i = 0; i < applications.length; i++) {
            const app = applications[i];

            // اگر مدت زمان انجام ثبت شده باشد، آن را هم نشان بده
            let durationHtml = "";
            if (app.duration_days) {
                durationHtml = `<span><i class="fa-solid fa-clock"></i> مدت انجام: ${formatNumber(app.duration_days)} روز</span>`;
            }

            // عنوان پروژه اگر آیدی پروژه را داشتیم لینک می‌شود
            let titleHtml = escapeHtml(app.project_title);
            if (app.project) {
                titleHtml = `<a href="project-detail.html?id=${escapeHtml(app.project)}">${escapeHtml(app.project_title)}</a>`;
            }

            html += `
                <div class="item-card">
                    <div class="item-top">
                        <p class="item-title">${titleHtml}</p>
                        <span class="status-badge ${statusClass(app.status)}">${bidStatusFa(app.status)}</span>
                    </div>
                    <div class="item-meta">
                        <span><i class="fa-solid fa-user"></i> کارفرما: ${escapeHtml(app.project_owner_name)}</span>
                        <span><i class="fa-solid fa-coins"></i> قیمت پیشنهادی: ${formatNumber(app.proposed_price)}</span>
                        ${durationHtml}
                        <span><i class="fa-solid fa-calendar"></i> ${formatDate(app.created_at)}</span>
                    </div>
                </div>
            `;
        }

        myApplicationsList.innerHTML = html;

    } catch (error) {
        if (isNotFound(error)) {
            myApplicationsList.innerHTML = "<p class='empty-text'>این بخش هنوز روی سرور فعال نشده است.</p>";
            return;
        }
        console.error("خطا در دریافت درخواست‌های من:", error);
        myApplicationsList.innerHTML = "<p class='field-error show'>خطا در دریافت درخواست‌ها.</p>";
    }
}

// ===== پروژه‌های ذخیره‌شده =====
async function loadFavorites() {
    favoritesList.innerHTML = "<p class='loading-text'>در حال بارگذاری...</p>";

    try {
        const data = await apiRequest(ENDPOINTS.favorites);
        const favorites = getItems(data);

        if (favorites.length === 0) {
            favoritesList.innerHTML = "<p class='empty-text'>هنوز پروژه‌ای ذخیره نکرده‌اید.</p>";
            return;
        }

        let html = "";

        for (let i = 0; i < favorites.length; i++) {
            const fav = favorites[i];

            html += `
                <div class="item-card">
                    <div class="item-top">
                        <p class="item-title">
                            <a href="project-detail.html?id=${escapeHtml(fav.project)}">${escapeHtml(fav.project_title)}</a>
                        </p>
                    </div>
                    <div class="item-meta">
                        <span><i class="fa-solid fa-user"></i> کارفرما: ${escapeHtml(fav.project_owner_name)}</span>
                        <span><i class="fa-solid fa-calendar"></i> ذخیره‌شده در: ${formatDate(fav.created_at)}</span>
                    </div>
                    <div class="item-actions">
                        <button type="button" class="revoke-btn" data-id="${escapeHtml(fav.project)}">حذف از ذخیره‌شده‌ها</button>
                    </div>
                </div>
            `;
        }

        favoritesList.innerHTML = html;

        // به دکمه‌های «حذف از ذخیره‌شده‌ها» گوش بده
        const removeButtons = favoritesList.querySelectorAll(".revoke-btn");
        removeButtons.forEach(function (button) {
            button.addEventListener("click", function () {
                removeFavorite(button.dataset.id);
            });
        });

    } catch (error) {
        if (isNotFound(error)) {
            favoritesList.innerHTML = "<p class='empty-text'>این بخش هنوز روی سرور فعال نشده است.</p>";
            return;
        }
        console.error("خطا در دریافت ذخیره‌شده‌ها:", error);
        favoritesList.innerHTML = "<p class='field-error show'>خطا در دریافت پروژه‌های ذخیره‌شده.</p>";
    }
}

// حذف یک پروژه از ذخیره‌شده‌ها
// همان endpoint مربوط به toggle است؛ چون پروژه الان ذخیره است، صدازدنش یعنی حذف
async function removeFavorite(projectId) {
    try {
        const response = await fetch(BASE_URL + ENDPOINTS.favorites + projectId + "/toggle/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + localStorage.getItem("access")
            }
        });

        if (response.ok) {
            // لیست را دوباره بگیر تا پروژه‌ی حذف‌شده دیده نشود
            loadFavorites();
        } else {
            console.error("خطا در حذف پروژه‌ی ذخیره‌شده. وضعیت:", response.status);
        }

    } catch (error) {
        console.error("خطا:", error);
    }
}

// ===== پروفایل کاربر =====
const profileForm = document.getElementById("profile-form");

async function loadProfile() {
    try {
        const data = await apiRequest(ENDPOINTS.profile);

        document.getElementById("profile-email").value = data.email || "";
        document.getElementById("profile-first-name").value = data.first_name || "";
        document.getElementById("profile-last-name").value = data.last_name || "";
        document.getElementById("profile-phone").value = data.phone || "";
        document.getElementById("profile-gender").value = data.gender || "male";
        document.getElementById("profile-birth").value = data.date_of_birth || "";

        // اسم و ایمیل را در منوی کناری هم نشان بده
        sidebarUserName.textContent = data.full_name || "";
        sidebarUserEmail.textContent = data.email || "";

    } catch (error) {
        console.error("خطا در دریافت پروفایل:", error);
        showFieldError("error-profile-form", "خطا در دریافت اطلاعات پروفایل.");
    }
}

profileForm.addEventListener("submit", async function (event) {
    event.preventDefault();
    clearFormMessages(profileForm);

    const body = {
        first_name: document.getElementById("profile-first-name").value,
        last_name: document.getElementById("profile-last-name").value,
        phone: document.getElementById("profile-phone").value,
        gender: document.getElementById("profile-gender").value,
        date_of_birth: document.getElementById("profile-birth").value || null
    };

    try {
        // برای فرم‌ها fetch خام می‌زنیم تا خطاهای فیلدیِ سرور را بخوانیم
        const response = await fetch(BASE_URL + ENDPOINTS.profile, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + localStorage.getItem("access")
            },
            body: JSON.stringify(body)
        });

        const data = await response.json();

        if (response.ok) {
            const success = document.getElementById("success-profile");
            success.textContent = "پروفایل با موفقیت به‌روزرسانی شد.";
            success.classList.add("show");

            sidebarUserName.textContent = data.full_name || "";
            return;
        }

        // خطاهای فیلدی سرور
        if (data.first_name) showFieldError("error-first_name", data.first_name[0]);
        if (data.last_name) showFieldError("error-last_name", data.last_name[0]);
        if (data.phone) showFieldError("error-phone", data.phone[0]);
        if (data.gender) showFieldError("error-gender", data.gender[0]);
        if (data.date_of_birth) showFieldError("error-date_of_birth", data.date_of_birth[0]);
        if (data.detail) showFieldError("error-profile-form", data.detail);

    } catch (error) {
        showFieldError("error-profile-form", "ارتباط با سرور برقرار نشد");
    }
});

// ===== پروفایل شرکت =====
const companyForm = document.getElementById("company-form");

// اگر شرکت وجود داشت PATCH می‌زنیم، وگرنه POST (ساخت شرکت جدید)
let companyExists = false;

async function loadCompany() {
    try {
        const data = await apiRequest(ENDPOINTS.company);

        companyExists = true;

        document.getElementById("company-name").value = data.name || "";
        document.getElementById("company-description").value = data.description || "";
        document.getElementById("company-website").value = data.website || "";
        document.getElementById("company-phone").value = data.phone || "";
        document.getElementById("company-address").value = data.address || "";

        // نشان «تأییدشده» فقط اگر شرکت تأیید شده باشد
        if (data.is_verified) {
            document.getElementById("companyVerified").classList.remove("hidden");
        }

    } catch (error) {
        // اگر شرکتی ثبت نشده باشد سرور خطا می‌دهد؛ فرم خالی می‌ماند و POST می‌زنیم
        companyExists = false;
        console.log("شرکتی ثبت نشده است؛ فرم برای ساخت شرکت جدید آماده است.");
    }
}

companyForm.addEventListener("submit", async function (event) {
    event.preventDefault();
    clearFormMessages(companyForm);

    const body = {
        name: document.getElementById("company-name").value,
        description: document.getElementById("company-description").value,
        website: document.getElementById("company-website").value || null,
        phone: document.getElementById("company-phone").value,
        address: document.getElementById("company-address").value
    };

    // اگر شرکت از قبل هست PATCH، وگرنه POST
    let method = "POST";
    if (companyExists) {
        method = "PATCH";
    }

    try {
        const response = await fetch(BASE_URL + ENDPOINTS.company, {
            method: method,
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + localStorage.getItem("access")
            },
            body: JSON.stringify(body)
        });

        const data = await response.json();

        if (response.ok) {
            companyExists = true;

            const success = document.getElementById("success-company");
            success.textContent = "اطلاعات شرکت با موفقیت ذخیره شد.";
            success.classList.add("show");
            return;
        }

        if (data.name) showFieldError("error-name", data.name[0]);
        if (data.description) showFieldError("error-description", data.description[0]);
        if (data.website) showFieldError("error-website", data.website[0]);
        if (data.phone) showFieldError("error-company-phone", data.phone[0]);
        if (data.address) showFieldError("error-address", data.address[0]);
        if (data.detail) showFieldError("error-company-form", data.detail);

    } catch (error) {
        showFieldError("error-company-form", "ارتباط با سرور برقرار نشد");
    }
});

// ===== نشست‌های فعال =====
async function loadSessions() {
    sessionsList.innerHTML = "<p class='loading-text'>در حال بارگذاری...</p>";

    try {
        const data = await apiRequest(ENDPOINTS.sessions);
        const userSessions = getItems(data);

        if (userSessions.length === 0) {
            sessionsList.innerHTML = "<p class='empty-text'>نشست فعالی وجود ندارد.</p>";
            return;
        }

        let html = "";

        for (let i = 0; i < userSessions.length; i++) {

            const session = userSessions[i];

            // اسم خلاصه‌ی دستگاه؛ user agent کامل در title می‌ماند تا با نگه‌داشتن موس دیده شود
            html += `
                <div class="item-card">
                    <div class="item-top">
                        <p class="item-title" title="${escapeHtml(session.user_agent)}">
                            <i class="fa-solid fa-desktop"></i>
                            ${escapeHtml(shortDeviceName(session.user_agent))}
                        </p>
                    </div>
                    <div class="item-meta">
                        <span><i class="fa-solid fa-location-dot"></i> IP: ${escapeHtml(session.ip_address || "—")}</span>
                        <span><i class="fa-solid fa-calendar"></i> شروع: ${formatDate(session.created_at)}</span>
                        <span><i class="fa-solid fa-hourglass-end"></i> انقضا: ${formatDate(session.expires_at)}</span>
                    </div>
                    <div class="item-actions">
                        <button type="button" class="revoke-btn" data-id="${escapeHtml(session.id)}">خروج از این نشست</button>
                    </div>
                </div>
            `;
        }

        sessionsList.innerHTML = html;

        // به دکمه‌های «خروج از نشست» گوش بده
        const revokeButtons = sessionsList.querySelectorAll(".revoke-btn");
        revokeButtons.forEach(function (button) {
            button.addEventListener("click", function () {
                revokeSession(button.dataset.id);
            });
        });

    } catch (error) {
        if (isNotFound(error)) {
            sessionsList.innerHTML = "<p class='empty-text'>این بخش هنوز روی سرور فعال نشده است.</p>";
            return;
        }
        console.error("خطا در دریافت نشست‌ها:", error);
        sessionsList.innerHTML = "<p class='field-error show'>خطا در دریافت نشست‌ها.</p>";
    }
}

async function revokeSession(sessionId) {
    try {
        const response = await fetch(BASE_URL + ENDPOINTS.sessions + sessionId + "/revoke/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + localStorage.getItem("access")
            }
        });

        if (response.ok) {
            // لیست را دوباره بگیر تا نشست حذف‌شده دیده نشود
            loadSessions();
        } else {
            console.error("خطا در خروج از نشست. وضعیت:", response.status);
        }

    } catch (error) {
        console.error("خطا:", error);
    }
}

// ===== تغییر رمز عبور =====
const passwordForm = document.getElementById("password-form");

passwordForm.addEventListener("submit", async function (event) {
    event.preventDefault();
    clearFormMessages(passwordForm);

    const body = {
        old_password: document.getElementById("old-password").value,
        new_password: document.getElementById("new-password").value,
        confirm_password: document.getElementById("confirm-password").value
    };

    try {
        const response = await fetch(BASE_URL + ENDPOINTS.changePassword, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + localStorage.getItem("access")
            },
            body: JSON.stringify(body)
        });

        const data = await response.json();

        if (response.ok) {
            const success = document.getElementById("success-password");
            success.textContent = "رمز عبور با موفقیت تغییر کرد.";
            success.classList.add("show");

            passwordForm.reset();
            return;
        }

        if (data.old_password) showFieldError("error-old_password", data.old_password[0]);
        if (data.new_password) showFieldError("error-new_password", data.new_password[0]);
        if (data.confirm_password) showFieldError("error-confirm_password", data.confirm_password[0]);
        if (data.detail) showFieldError("error-password-form", data.detail);

    } catch (error) {
        showFieldError("error-password-form", "ارتباط با سرور برقرار نشد");
    }
});

// ===== شروع: خلاصه وضعیت، نمودار فعالیت و اطلاعات کاربر برای منوی کناری =====
loadedSections["section-summary"] = true;
loadSummary();
loadActivityChart();
loadProfile();
