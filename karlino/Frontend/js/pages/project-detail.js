// این فایل فقط برای صفحه‌ی جزئیات پروژه است: project-detail.html

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


// ۴) پرکردن صفحه با اطلاعات پروژه
function renderProject(project) {
  // عنوان
  document.getElementById("project-title").textContent = project.title;

  // نام صاحب پروژه (این فیلد خودش حالت شرکت یا شخص را مدیریت می‌کند)
  document.getElementById("owner-name").textContent = project.display_owner_name;

  // توضیحات
  document.getElementById("project-about-text").textContent = project.description;

  // چند روز پیش ثبت شده
  document.getElementById("project-days").textContent = daysAgoText(project.created_at);

  // بودجه
  document.getElementById("project-budget").textContent = budgetText(project.budget_min, project.budget_max);

  // سطح مهارت
  // توجه: این فیلد هنوز از طرف بک‌اند نهایی نشده. اسم دقیق فیلد را از بک‌اند بپرس
  // و اگر اسمش چیز دیگری بود، اینجا project.skill_level را عوض کن.
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

  // اگر پروژه فعال نباشد، اجازه‌ی ارسال درخواست نده
  if (project.status !== "active") {
    const applyButton = document.getElementById("apply-button");
    applyButton.disabled = true;
    document.getElementById("apply-button-text").textContent = "این پروژه بسته شده است";
  }
}


// --- توابع کمکی ---

// تبدیل تاریخ ثبت به متن «n روز پیش»
function daysAgoText(createdAt) {
  if (!createdAt) {
    return "";
  }
  const created = new Date(createdAt);
  const now = new Date();
  const oneDay = 1000 * 60 * 60 * 24;
  const days = Math.floor((now - created) / oneDay);

  if (days <= 0) {
    return "امروز";
  }
  return days + " روز پیش";
}


// ساخت متن بودجه با مدیریت حالت خالی
function budgetText(min, max) {
  // اگر هیچ‌کدام مقدار نداشت
  if (!min && !max) {
    return "توافقی";
  }

  let text = "";
  if (min) {
    text = text + Number(min).toLocaleString("fa-IR");
  }
  if (min && max) {
    text = text + " - ";
  }
  if (max) {
    text = text + Number(max).toLocaleString("fa-IR");
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


// --- فرم ارسال درخواست ---
function setupApplyForm() {
  const button = document.getElementById("apply-button");
  const formBox = document.getElementById("apply-form-box");
  const submit = document.getElementById("apply-submit");

  // با کلیک روی دکمه‌ی اصلی، فرم باز شود
  button.addEventListener("click", function () {
    const token = localStorage.getItem("access");

    if (!token) {
      window.location.href = "login.html";
      return;
    }

    formBox.style.display = "block";
  });

  // با کلیک روی «ثبت»، درخواست فرستاده شود
  submit.addEventListener("click", async function () {
    const coverLetter = document.getElementById("cover-letter").value;
    const proposedPrice = document.getElementById("proposed-price").value;
    const messageBox = document.getElementById("apply-message");
    const token = localStorage.getItem("access");

    const body = {
      cover_letter: coverLetter,
      proposed_price: proposedPrice,
    };

    // اینجا از fetch خام استفاده می‌کنیم (نه apiRequest)
    // چون می‌خواهیم خطاهای فیلدی بک‌اند را بخوانیم
    const res = await fetch(BASE_URL + ENDPOINTS.projects + projectId + "/apply/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token,
      },
      body: JSON.stringify(body),
    });

    const data = await res.json();

    if (res.ok) {
      messageBox.textContent = "درخواست شما با موفقیت ثبت شد.";
    } else {
      // نمایش خطای بک‌اند
      if (data.detail) {
        messageBox.textContent = data.detail;
      } else if (data.cover_letter) {
        messageBox.textContent = data.cover_letter[0];
      } else {
        messageBox.textContent = "ثبت درخواست با خطا روبه‌رو شد.";
      }
    }
  });
}