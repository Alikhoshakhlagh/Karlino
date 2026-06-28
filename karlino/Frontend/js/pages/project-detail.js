
// ۱) خواندن id پروژه از آدرس صفحه
// آدرس به این شکل است: project-detail.html?id=<شناسه‌ی پروژه>
const params = new URLSearchParams(window.location.search);
const projectId = params.get("id");


// ۲) شروع کار
// اگر اصلا id در آدرس نبود، پیام خطا نشان بده
if (!projectId) {
  const container = document.querySelector(".container-project");
  container.textContent = "آدرس پروژه نامعتبر است.";
} else {
  loadProject();
  setupFavorite();
  setupApplyForm();
}


// ۳) گرفتن اطلاعات این پروژه‌ی خاص از سرور
async function loadProject() {
  // مسیر این پروژه: /api/projects/<id>/
  // apiRequest خودش BASE_URL را جلوی مسیر می‌گذارد، پس فقط مسیر را می‌دهیم
  const project = await apiRequest(ENDPOINTS.projects + projectId + "/");

  // اگر پروژه پیدا نشد یا پاسخ معتبر نبود
  if (!project || !project.id) {
    const container = document.querySelector(".container-project");
    container.textContent = "پروژه پیدا نشد.";
    return;
  }

  renderProject(project);
}


function renderProject(project) {
  document.getElementById("project-title").textContent = project.title;

  document.getElementById("owner-name").textContent = project.display_owner_name;

  document.getElementById("project-about-text").textContent = project.description;

  // «چند روز پیش» مستقیم از بک‌اند می‌آید، پس همان را نشان می‌دهیم
  if (project.project_age_days) {
    document.getElementById("project-days").textContent = project.project_age_days;
  } else {
    document.getElementById("project-days").textContent = "";
  }

  document.getElementById("project-budget").textContent = budgetText(project.budget_min, project.budget_max);

  // سطح مهارت
  if (project.skill_level) {
    document.getElementById("project-skill-level").textContent = project.skill_level;
  } else {
    document.getElementById("project-skill-level").textContent = "نامشخص";
  }

  // مهلت انجام
  document.getElementById("project-deadline").textContent = deadlineText(project.deadline);

  // مهارت‌ها
  renderSkills(project.skills);

  // دسته‌بندی‌ها
  renderCategories(project.categories_data);
}


// --- توابع کمکی ---

// ساخت متن بودجه با مدیریت حالت خالی
function budgetText(min, max) {
  // اگر هیچ‌کدام مقدار نداشت
  if (!min && !max) {
    return "توافقی";
  }

  let text = "";
  if (min) {
    text = text + Number(min)
  }
  if (min && max) {
    text = text + " - ";
  }
  if (max) {
    text = text + Number(max)
  }
  return text + " تومان";
}


// تبدیل تاریخ مهلت به تاریخ شمسی
function deadlineText(deadline) {
  if (!deadline) {
    return "نامشخص";
  }
  const d = new Date(deadline);
  return d.toLocaleDateString("fa-IR");
}


// ساخت چیپ‌های مهارت
function renderSkills(skills) {
  const container = document.getElementById("project-skills-list");
  container.innerHTML = ""; // پاک‌کردن هر چیز قبلی

  if (!skills || skills.length === 0) {
    const p = document.createElement("p");
    p.textContent = "ثبت نشده";
    container.appendChild(p);
    return;
  }

  for (let i = 0; i < skills.length; i++) {
    const skill = skills[i];
    const p = document.createElement("p");

    // مهارت ممکن است رشته‌ی ساده باشد یا آبجکتی با فیلد name
    if (typeof skill === "string") {
      p.textContent = skill;
    } else {
      p.textContent = skill.name;
    }

    container.appendChild(p);
  }
}


// ساخت چیپ‌های دسته‌بندی
function renderCategories(categories) {
  const container = document.getElementById("project-categories-list");
  container.innerHTML = "";

  if (!categories || categories.length === 0) {
    const p = document.createElement("p");
    p.textContent = "ثبت نشده";
    container.appendChild(p);
    return;
  }

  for (let i = 0; i < categories.length; i++) {
    const category = categories[i];
    const p = document.createElement("p");
    p.textContent = category.name;
    container.appendChild(p);
  }
}


// --- دکمه‌ی ذخیره (bookmark) ---
function setupFavorite() {
  const checkbox = document.getElementById("bookmark-checkbox");

  checkbox.addEventListener("change", async function () {
    const token = localStorage.getItem("access");

    // ذخیره‌کردن نیاز به لاگین دارد
    if (!token) {
      window.location.href = "login.html";
      return;
    }

    // صدا زدن endpoint مربوط به toggle این پروژه
    await apiRequest(ENDPOINTS.favorites + projectId + "/toggle/", {
      method: "POST",
      body: JSON.stringify({}),
    });
  });
}


