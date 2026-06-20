// ===== المنت‌ها =====
const projectsContainer = document.getElementById("projectsContainer");
const paginationContainer = document.querySelector(".project-pagination");
const searchInput = document.getElementById("query");

const sortBox = document.querySelector(".sort-box");
const selectedOption = document.querySelector(".selected-option");
const optionsContainer = document.querySelector(".options-container");
const options = document.querySelectorAll(".option");

const confirmFilterBtn = document.querySelector(".confirm-filter");
const clearFilterBtn = document.querySelector(".clear-filter");

// دو ظرف فیلتر: اولی دسته‌بندی، دومی مهارت
const filterContainers = document.querySelectorAll(".filter-box .items-container");
const categoryFiltersContainer = filterContainers[0];
const skillFiltersContainer = filterContainers[1];

// ===== متغیرهای وضعیت =====
let allProjects = [];
let allCategories = [];
let allSkills = [];
let filteredProjects = [];

let pageSize = 1;
let currentPage = 1;
let currentSort = "جدیدترین ها";

let activeCategoryFilters = [];
let activeSkillFilters = [];

// ===== گرفتن همه‌ی صفحه‌های یک endpoint =====
async function fetchAll(url) {
    let allItems = [];
    let firstSize = 0;
    let isFirst = true;

    while (url) {
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error("خطا در دریافت اطلاعات");
        }

        const data = await response.json();

        if (isFirst) {
            firstSize = data.results.length;
            isFirst = false;
        }

        for (let i = 0; i < data.results.length; i++) {
            allItems.push(data.results[i]);
        }

        url = data.next;
    }

    return {
        items: allItems,
        firstSize: firstSize
    };
}

// ===== ساختن چک‌باکس‌های دسته‌بندی =====
function renderCategoryFilters() {
    let html = "";

    for (let i = 0; i < allCategories.length; i++) {
        const cat = allCategories[i];

        html += `
            <div class="item">
                <input type="checkbox" id="cat-${cat.id}" data-id="${cat.id}" hidden />
                <label for="cat-${cat.id}" class="check">
                    <i class="fa-solid fa-check"></i>
                </label>
                <span>${cat.name}</span>
            </div>
        `;
    }

    categoryFiltersContainer.innerHTML = html;
}

// ===== ساختن چک‌باکس‌های مهارت =====
function renderSkillFilters() {
    let html = "";

    for (let i = 0; i < allSkills.length; i++) {
        const skill = allSkills[i];

        html += `
            <div class="item">
                <input type="checkbox" id="skill-${skill.id}" data-id="${skill.id}" hidden />
                <label for="skill-${skill.id}" class="check">
                    <i class="fa-solid fa-check"></i>
                </label>
                <span>${skill.name}</span>
            </div>
        `;
    }

    skillFiltersContainer.innerHTML = html;
}

// ===== گرفتن id چک‌باکس‌های تیک‌خورده =====
function getCheckedIds(container) {
    const result = [];
    const checkboxes = container.querySelectorAll("input[type='checkbox']");

    for (let i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {
            result.push(checkboxes[i].dataset.id);
        }
    }

    return result;
}

// ===== اعمال جستجو + فیلتر + مرتب‌سازی =====
function applyAll() {
    let result = [];

    for (let i = 0; i < allProjects.length; i++) {
        result.push(allProjects[i]);
    }

    // 1) جستجو روی عنوان
    const searchText = searchInput.value.trim().toLowerCase();

    if (searchText !== "") {
        let temp = [];

        for (let i = 0; i < result.length; i++) {
            const title = String(result[i].title || "").toLowerCase();

            if (title.includes(searchText)) {
                temp.push(result[i]);
            }
        }

        result = temp;
    }

    // 2) فیلتر دسته‌بندی (بر اساس دسته‌ی اصلی پروژه)
    if (activeCategoryFilters.length > 0) {
        let temp = [];

        for (let i = 0; i < result.length; i++) {
            const project = result[i];

            let primaryCategoryId = null;

            if (project.primary_category_data && project.primary_category_data.id != null) {
                primaryCategoryId = String(project.primary_category_data.id);
            } else if (project.primary_category != null) {
                primaryCategoryId = String(project.primary_category);
            }

            for (let j = 0; j < activeCategoryFilters.length; j++) {
                if (primaryCategoryId === activeCategoryFilters[j]) {
                    temp.push(project);
                    break;
                }
            }
        }

        result = temp;
    }

    // 3) فیلتر مهارت (اگر پروژه حداقل یکی از مهارت‌های انتخاب‌شده را داشته باشد)
    if (activeSkillFilters.length > 0) {
        let temp = [];

        for (let i = 0; i < result.length; i++) {
            const project = result[i];
            const skills = project.skills || [];

            let found = false;

            for (let j = 0; j < skills.length; j++) {
                for (let k = 0; k < activeSkillFilters.length; k++) {
                    if (String(skills[j].id) === activeSkillFilters[k]) {
                        found = true;
                    }
                }
            }

            if (found) {
                temp.push(project);
            }
        }

        result = temp;
    }

    // 4) مرتب‌سازی
    if (currentSort.includes("محبوب")) {
        result.sort(function (a, b) {
            return (b.favorites_count || 0) - (a.favorites_count || 0);
        });
    } else if (currentSort.includes("بالا")) {
        result.sort(function (a, b) {
            return Number(b.budget_max || 0) - Number(a.budget_max || 0);
        });
    } else if (currentSort.includes("کم")) {
        result.sort(function (a, b) {
            return Number(a.budget_min || 0) - Number(b.budget_min || 0);
        });
    } else {
        result.sort(function (a, b) {
            return new Date(b.created_at) - new Date(a.created_at);
        });
    }

    filteredProjects = result;
    renderPage(1);
}

// ===== نمایش یک صفحه =====
function renderPage(page) {
    currentPage = page;

    const start = (page - 1) * pageSize;
    const end = start + pageSize;

    let pageItems = [];
    for (let i = start; i < end && i < filteredProjects.length; i++) {
        pageItems.push(filteredProjects[i]);
    }

    if (pageItems.length === 0) {
        projectsContainer.innerHTML = "<p>پروژه‌ای پیدا نشد.</p>";
        paginationContainer.innerHTML = "";
        return;
    }

    let html = "";

    for (let i = 0; i < pageItems.length; i++) {
        const project = pageItems[i];

        const primaryCategoryId = project.primary_category_data?.id;
        const icon = project.primary_category_data?.icon || "fa-solid fa-folder";
        const primaryCategoryName = project.primary_category_data?.name || "بدون دسته‌بندی";

        const others = (project.categories_data || []).filter(function (cat) {
            return cat.id !== primaryCategoryId;
        });

        let otherCategoriesHtml = "";
        for (let j = 0; j < others.length; j++) {
            otherCategoriesHtml += `<p>${others[j].name}</p>`;
        }

        const budgetMin = Number(project.budget_min || 0).toLocaleString();
        const budgetMax = Number(project.budget_max || 0).toLocaleString();

        const createdAt = project.created_at
            ? new Date(project.created_at).toLocaleDateString("fa-IR")
            : "-";

        html += `
            <div class="card-project">
                <div class="card-top">
                    <div class="icon-project">
                        <span><i class="${icon}"></i></span>
                    </div>

                    <div class="status-project">
                        <span class="active">${project.status || ""}</span>
                    </div>

                    <label for="checkbox-${project.id}" class="bookmark">
                        <input type="checkbox" id="checkbox-${project.id}" data-id="${project.id}" />
                        <svg width="15" viewBox="0 0 50 70" fill="none" xmlns="http://www.w3.org/2000/svg" class="svgIcon">
                            <path d="M46 62.0085L46 3.88139L3.99609 3.88139L3.99609 62.0085L24.5 45.5L46 62.0085Z" stroke="black" stroke-width="7"></path>
                        </svg>
                    </label>
                </div>

                <div class="card-content">
                    <h2 class="owner">
                        <i class="fa-solid fa-user"></i>
                        ${project.display_owner_name || ""}
                    </h2>

                    <h3>${project.title || ""}</h3>

                    <div class="card-pro-cat">
                        <p>${primaryCategoryName}</p>
                        <p>${(project.categories_data || [])
            .find(cat => cat.id !== project.primary_category_data?.id)

            ?.name || ""
        }

</p>
                    </div>

                    <div class="price">
                        <span>تومان</span>
                        <span class="number">
                            ${budgetMin}
                            -
                            ${budgetMax}
                        </span>
                    </div>
                </div>

                <div class="card-footer">
                    <span class="daysAgo">
                        ${project.project_age_days}
                    </span>

                    <button class="button project-details-btn" data-id="${project.id}" type="button">
                        <div class="button-box">
                            <span class="button-elem">
                                <svg viewBox="0 0 46 40" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M46 20.038c0-.7-.3-1.5-.8-2.1l-16-17c-1.1-1-3.2-1.4-4.4-.3-1.2 1.1-1.2 3.3 0 4.4l11.3 11.9H3c-1.7 0-3 1.3-3 3s1.3 3 3 3h33.1l-11.3 11.9c-1 1-1.2 3.3 0 4.4 1.2 1.1 3.3.8 4.4-.3l16-17c.5-.5.8-1.1.8-1.9z"></path>
                                </svg>
                            </span>
                            <span class="button-elem">
                                <svg viewBox="0 0 46 40">
                                    <path d="M46 20.038c0-.7-.3-1.5-.8-2.1l-16-17c-1.1-1-3.2-1.4-4.4-.3-1.2 1.1-1.2 3.3 0 4.4l11.3 11.9H3c-1.7 0-3 1.3-3 3s1.3 3 3 3h33.1l-11.3 11.9c-1 1-1.2 3.3 0 4.4 1.2 1.1 3.3.8 4.4-.3l16-17c.5-.5.8-1.1.8-1.9z"></path>
                                </svg>
                            </span>
                        </div>
                    </button>
                </div>
            </div>
        `;
    }

    projectsContainer.innerHTML = html;
    renderPagination();
    window.scrollTo(0, 0);

    if (typeof initBookmarks === "function") {
        initBookmarks();
    }

    const detailButtons = document.querySelectorAll(".project-details-btn");
    for (let i = 0; i < detailButtons.length; i++) {
        detailButtons[i].addEventListener("click", function () {
            const id = detailButtons[i].dataset.id;
            window.location.href = `/project-details.html?id=${id}`;
        });
    }
}

// ===== دکمه‌های صفحه‌بندی =====
function renderPagination() {
    const totalPages = Math.ceil(filteredProjects.length / pageSize);

    paginationContainer.innerHTML = "";
    if (totalPages <= 1) return;

    // فلش قبلی
    const prevBtn = document.createElement("button");
    prevBtn.className = "page-btn arrow-btn";
    prevBtn.innerHTML = `<i class="fa-solid fa-angle-right"></i>`;
    prevBtn.disabled = currentPage === 1;
    prevBtn.addEventListener("click", function () {
        renderPage(currentPage - 1);
    });
    paginationContainer.appendChild(prevBtn);

    // دکمه‌های شماره
    for (let i = 1; i <= totalPages; i++) {
        const button = document.createElement("button");
        button.className = "page-btn";

        if (i === currentPage) {
            button.classList.add("active");
        }

        button.textContent = i;
        button.addEventListener("click", function () {
            renderPage(i);
        });

        paginationContainer.appendChild(button);
    }

    // فلش بعدی
    const nextBtn = document.createElement("button");
    nextBtn.className = "page-btn arrow-btn";
    nextBtn.innerHTML = `<i class="fa-solid fa-angle-left"></i>`;
    nextBtn.disabled = currentPage === totalPages;
    nextBtn.addEventListener("click", function () {
        renderPage(currentPage + 1);
    });
    paginationContainer.appendChild(nextBtn);
}

// ===== Sort Box =====
selectedOption.addEventListener("click", function () {
    optionsContainer.classList.toggle("show");
});

for (let i = 0; i < options.length; i++) {
    options[i].addEventListener("click", function () {
        currentSort = options[i].textContent.trim();
        selectedOption.innerHTML = currentSort + ` <i class="fa-solid fa-angle-down"></i>`;
        optionsContainer.classList.remove("show");
        applyAll();
    });
}

document.addEventListener("click", function (event) {
    if (!sortBox.contains(event.target)) {
        optionsContainer.classList.remove("show");
    }
});

// ===== جستجو =====
searchInput.addEventListener("input", function () {
    applyAll();
});

// ===== اعمال فیلتر =====
confirmFilterBtn.addEventListener("click", function () {
    activeCategoryFilters = getCheckedIds(categoryFiltersContainer);
    activeSkillFilters = getCheckedIds(skillFiltersContainer);
    applyAll();
});

// ===== پاک کردن فیلتر =====
clearFilterBtn.addEventListener("click", function () {
    const allCheckboxes = document.querySelectorAll(".project-sidebar input[type='checkbox']");

    for (let i = 0; i < allCheckboxes.length; i++) {
        allCheckboxes[i].checked = false;
    }

    activeCategoryFilters = [];
    activeSkillFilters = [];

    applyAll();
});

// ===== شروع =====
async function init() {
    projectsContainer.innerHTML = "<p>در حال بارگذاری...</p>";

    try {
        const projectsResult = await fetchAll("http://127.0.0.1:8000/api/projects/");
        allProjects = projectsResult.items;
        pageSize = projectsResult.firstSize || allProjects.length || 1;

        const categoriesResult = await fetchAll("http://127.0.0.1:8000/api/categories/");
        allCategories = categoriesResult.items;

        const skillsResult = await fetchAll("http://127.0.0.1:8000/api/skills/");
        allSkills = skillsResult.items;

        renderCategoryFilters();
        renderSkillFilters();

        // ── اگر کاربر از هدر روی یک دسته‌بندی زده، از آدرس بخوان ──
        const params = new URLSearchParams(window.location.search);
        const categoryFromUrl = params.get("category");

        if (categoryFromUrl) {
            // چک‌باکس آن دسته‌بندی را تیک بزن
            const checkbox = categoryFiltersContainer.querySelector(
                `input[data-id="${categoryFromUrl}"]`
            );
            if (checkbox) {
                checkbox.checked = true;
                activeCategoryFilters = [categoryFromUrl]; // فیلتر را فعال کن (بدون زدن دکمه)
            }
        }

        applyAll(); // خودکار فیلتر و نمایش

    } catch (error) {
        console.error("خطا:", error);
        projectsContainer.innerHTML = "<p class='field-error'>خطا در دریافت اطلاعات.</p>";
    }
}

init();

