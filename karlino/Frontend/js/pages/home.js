// ===== پرطرفدارترین دسته‌بندی‌ها — از API =====

const categoriesContainer = document.getElementById("categoriesContainer");

async function loadCategories() {
    categoriesContainer.innerHTML = "<p>در حال بارگذاری...</p>";

    try {
        const response = await fetch("http://127.0.0.1:8000/api/categories/");
        if (!response.ok) throw new Error("خطا در دریافت اطلاعات");

        const data = await response.json();
        const categories = data.results;

        if (!categories.length) {
            categoriesContainer.innerHTML = "<p>دسته‌بندی‌ای موجود نیست.</p>";
            return;
        }

        categoriesContainer.innerHTML = "";

        categories.slice(0, 10).forEach((category) => {
            categoriesContainer.innerHTML += `
                <div class="card-Categories">
                    <div class="icon-cat">
                        <span>
                            <i class="${category.icon}"></i>
                        </span>
                    </div>
                    <div class="name-cat">
                        <p>${category.name}</p>
                    </div>
                </div>
            `;
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
        const response = await fetch("http://127.0.0.1:8000/api/projects/");
        if (!response.ok) throw new Error("خطا در دریافت اطلاعات");

        const data = await response.json();
        const projects = data.results;

        if (!projects.length) {
            projectsContainer.innerHTML = "<p>پروژه‌ای موجود نیست.</p>";
            return;
        }

        projectsContainer.innerHTML = "";

        projects.slice(0, 8).forEach((project, index) => {

            // دسته‌بندی‌های اضافی (بدون تکرارِ دسته‌ی اصلی)
            const others = (project.categories_data || [])
                .filter(cat => cat.id !== project.primary_category_data.id);

            projectsContainer.innerHTML += `
                <div class="card-project">

                    <div class="card-top">

                        <div class="icon-project">
                            <span>
                                <i class="${project.primary_category_data.icon}"></i>
                            </span>
                        </div>

                        <div class="status-project">
                            <span class="active">${project.status}</span>
                        </div>

                        <label for="checkbox-${index}" class="bookmark">
                            <input
                                type="checkbox"
                                id="checkbox-${index}"
                                data-id="${project.id}"
                            />
                            <svg
                                width="15"
                                viewBox="0 0 50 70"
                                fill="none"
                                xmlns="http://www.w3.org/2000/svg"
                                class="svgIcon"
                            >
                                <path
                                    d="M46 62.0085L46 3.88139L3.99609 3.88139L3.99609 62.0085L24.5 45.5L46 62.0085Z"
                                    stroke="black"
                                    stroke-width="7"
                                ></path>
                            </svg>
                        </label>

                    </div>

                    <div class="card-content">

                        <h2 class="owner">
                            <i class="fa-solid fa-user"></i>
                            ${project.display_owner_name}
                        </h2>

                        <h3>${project.title}</h3>

                        <div class="card-pro-cat">
                            <p>${project.primary_category_data.name}</p>
                            ${others.map(cat => `<p>${cat.name}</p>`).join("")}
                        </div>

                        <div class="price">
                            <span>تومان</span>
                            <span class="number">
                                ${Number(project.budget_min).toLocaleString()}
                                -
                                ${Number(project.budget_max).toLocaleString()}
                            </span>
                        </div>

                    </div>

                    <div class="card-footer">

                        <span class="daysAgo">
                            ${new Date(project.created_at).toLocaleDateString("fa-IR")}
                        </span>

                        <button class="button" type="button">
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
        });

        // ← مهم: بعد از ساختن کارت‌ها، بوکمارک‌ها را راه‌اندازی کن
        // (هم به کلیک‌ها گوش می‌دهد، هم علاقه‌مندی‌های قبلی را تیک می‌زند)
        await initBookmarks();

    } catch (error) {
        console.error("خطا در دریافت پروژه‌ها:", error);
        projectsContainer.innerHTML =
            "<p class='field-error'>خطا در دریافت پروژه‌ها.</p>";
    }
}

loadProjects();