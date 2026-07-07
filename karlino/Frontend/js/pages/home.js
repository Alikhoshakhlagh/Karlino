// ===== پرطرفدارترین دسته‌بندی‌ها — از API =====

const categoriesContainer = document.getElementById("categoriesContainer");

async function loadCategories() {
    categoriesContainer.innerHTML = "<p>در حال بارگذاری...</p>";

    try {
        const response = await fetch(BASE_URL + ENDPOINTS.categories);
        if (!response.ok) throw new Error("خطا در دریافت اطلاعات");

        const data = await response.json();
        const categories = data.results;

        if (!categories.length) {
            categoriesContainer.innerHTML = "<p>دسته‌بندی‌ای موجود نیست.</p>";
            return;
        }

        categoriesContainer.innerHTML = "";

        categories.slice(0, 11).forEach((category) => {
            categoriesContainer.appendChild(
                createCategoryCard(category)
            );
        });

    } catch (error) {
        console.error("خطا در دریافت دسته‌بندی‌ها:", error);
        categoriesContainer.innerHTML =
            "<p class='field-error'>خطا در دریافت دسته‌بندی‌ها.</p>";
    }
}

loadCategories();


// ===== پروژه‌ها — از API =====

const projectsContainer = document.getElementById("projectsContainer");

async function loadProjects() {
    projectsContainer.innerHTML = "<p>در حال بارگذاری...</p>";

    try {
        const response = await fetch(BASE_URL + ENDPOINTS.projects);
        if (!response.ok) throw new Error("خطا در دریافت اطلاعات");

        const data = await response.json();
        const projects = data.results;

        if (!projects.length) {
            projectsContainer.innerHTML = "<p>پروژه‌ای موجود نیست.</p>";
            return;
        }

        // فقط ۸ تای اول را در صفحه‌ی خانه نشان می‌دهیم
        const visibleProjects = projects.slice(0, 8);

        // همه‌ی کارت‌ها را در یک رشته جمع می‌کنیم و یک‌بار در صفحه می‌گذاریم
        let html = "";
        for (let index = 0; index < visibleProjects.length; index++) {
            html += createProjectCard(visibleProjects[index]);
        }
        projectsContainer.innerHTML = html;

        // بعد از ساختن کارت‌ها، بوکمارک‌ها را راه‌اندازی کن
        await initBookmarks();

    } catch (error) {
        console.error("خطا در دریافت پروژه‌ها:", error);
        projectsContainer.innerHTML =
            "<p class='field-error'>خطا در دریافت پروژه‌ها.</p>";
    }
}

loadProjects();

// ===== جستجوی صفحه‌ی اصلی → هدایت به صفحه‌ی پروژه‌ها =====

const indexSearch = document.getElementById("indexSearch");
const indexSearchBtn = document.querySelector(".find-talent");

function goToProjectsSearch() {
    const text = indexSearch.value.trim();

    // اگر خالی بود، فقط برو صفحه‌ی پروژه‌ها بدون سرچ
    if (text === "") {
        window.location.href = "projects.html";
        return;
    }

    window.location.href = "projects.html?search=" + encodeURIComponent(text);
}

// Enter داخل کادر
if (indexSearch) {
    indexSearch.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            goToProjectsSearch();
        }
    });
}

// کلیک روی دکمه‌ی ذره‌بین
if (indexSearchBtn) {
    indexSearchBtn.addEventListener("click", function () {
        goToProjectsSearch();
    });
}