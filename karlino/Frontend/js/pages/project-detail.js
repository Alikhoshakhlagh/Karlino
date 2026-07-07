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

  // وضعیت دکمه‌ی «ارسال درخواست» را بر اساس پاسخ سرور تنظیم کن
  setupApplyState(project);
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

  // اسم پروژه را داخل پاپ‌آپ درخواست هم نشان بده
  document.getElementById("apply-project-name").textContent = "پروژه: " + project.title;
}


// وضعیت دکمه‌ی «ارسال درخواست»
// این اطلاعات از خود سرور می‌آید، پس حتی بعد از رفرش یا خروج و برگشت هم درست می‌ماند
function setupApplyState(project) {
  const applyButton = document.getElementById("apply-button");
  const applyButtonText = document.getElementById("apply-button-text");

  // اگر پروژه مال خود کاربر است، دکمه اصلا نشان داده نشود
  if (project.is_owner) {
    applyButton.style.display = "none";
    return;
  }

  // اگر کاربر قبلاً برای این پروژه درخواست داده، دکمه غیرفعال بماند
  if (project.has_applied) {
    applyButton.disabled = true;
    applyButtonText.textContent = "درخواست ارسال شد";
  }
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


// ===== پاپ‌آپ ارسال درخواست همکاری =====
function setupApplyForm() {

  const applyButton = document.getElementById("apply-button");
  const applyModal = document.getElementById("apply-modal");
  const applyOverlay = document.getElementById("apply-modal-overlay");
  const applyClose = document.getElementById("apply-close");
  const applyForm = document.getElementById("apply-form");

  // --- بازکردن پاپ‌آپ با دکمه‌ی «ارسال درخواست» ---
  applyButton.addEventListener("click", function () {

    // اگر دکمه غیرفعال است (قبلاً درخواست داده)، هیچ کاری نکن
    if (applyButton.disabled) {
      return;
    }

    // ارسال درخواست نیاز به لاگین دارد
    const token = localStorage.getItem("access");
    if (!token) {
      window.location.href = "login.html";
      return;
    }

    applyModal.classList.add("open");
  });

  // --- بستن پاپ‌آپ ---
  function closeModal() {
    applyModal.classList.remove("open");
  }

  applyClose.addEventListener("click", closeModal);
  applyOverlay.addEventListener("click", closeModal);

  // --- ارسال فرم ---
  applyForm.addEventListener("submit", async function (event) {

    event.preventDefault(); // جلوی رفرش‌شدن صفحه را می‌گیرد

    // پاک‌کردن پیام‌های دفعه‌ی قبل
    document.getElementById("error-cover_letter").textContent = "";
    document.getElementById("error-proposed_price").textContent = "";
    document.getElementById("error-duration_days").textContent = "";
    document.getElementById("error-apply-form").textContent = "";
    document.getElementById("success-apply").textContent = "";

    const token = localStorage.getItem("access");
    if (!token) {
      window.location.href = "login.html";
      return;
    }

    // قیمت و مدت زمان اختیاری هستند؛ اگر خالی بودند null بفرست
    const priceValue = document.getElementById("apply-price").value;
    const durationValue = document.getElementById("apply-duration").value;

    let proposedPrice = null;
    if (priceValue !== "") {
      proposedPrice = priceValue;
    }

    let durationDays = null;
    if (durationValue !== "") {
      durationDays = durationValue;
    }

    const body = {
      cover_letter: document.getElementById("apply-cover").value,
      proposed_price: proposedPrice,
      duration_days: durationDays
    };

    try {
      const response = await fetch(BASE_URL + ENDPOINTS.projects + projectId + "/apply/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer " + token
        },
        body: JSON.stringify(body)
      });

      const data = await response.json();

      // درخواست با موفقیت ثبت شد
      if (response.ok) {
        document.getElementById("success-apply").textContent =
          "درخواست شما با موفقیت ارسال شد. وضعیت آن را می‌توانید در پنل کاربری دنبال کنید.";

        applyForm.reset();

        // دکمه‌ی اصلی صفحه را غیرفعال کن و به حالت «ارسال شد» ببر
        // سرور هم از این به بعد has_applied را true برمی‌گرداند،
        // پس حتی بعد از خروج و برگشت هم دکمه غیرفعال می‌ماند
        applyButton.disabled = true;
        document.getElementById("apply-button-text").textContent = "درخواست ارسال شد";

        // بعد از ۲ ثانیه پاپ‌آپ را ببند تا کاربر پیام موفقیت را ببیند
        setTimeout(function () {
          closeModal();
          document.getElementById("success-apply").textContent = "";
        }, 2000);

        return;
      }

      // خطاهای فیلدی سرور
      if (data.cover_letter) {
        document.getElementById("error-cover_letter").textContent = data.cover_letter[0];
      }
      if (data.proposed_price) {
        document.getElementById("error-proposed_price").textContent = data.proposed_price[0];
      }
      if (data.duration_days) {
        document.getElementById("error-duration_days").textContent = data.duration_days[0];
      }

      // خطاهای کلی سرور (مثلاً: قبلاً درخواست داده‌اید / پروژه‌ی خودتان است)
      if (data.non_field_errors) {
        document.getElementById("error-apply-form").textContent = data.non_field_errors[0];
      }
      if (data.detail) {
        document.getElementById("error-apply-form").textContent = data.detail;
      }

    } catch (error) {
      document.getElementById("error-apply-form").textContent = "ارتباط با سرور برقرار نشد";
    }
  });
}
