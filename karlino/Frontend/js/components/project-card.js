// ────────────────────────────────────────────────────────────
// کامپوننت کارت پروژه
// این تابع داده‌ی یک پروژه را می‌گیرد و رشته‌ی HTML کارت آن را برمی‌گرداند.
// هم در home.js و هم در projects.js از همین یک تابع استفاده می‌شود
// تا کد کارت فقط یک‌جا نوشته شود و تکرار نشود.
//
// نکته‌ی لود: این فایل باید بعد از config.js (که escapeHtml در آن است)
// و قبل از home.js و projects.js در HTML لود شود.
// ────────────────────────────────────────────────────────────

function createProjectCard(project) {

    // ── ۱) آماده‌سازی داده‌ها قبل از ساختن HTML ──

    // دسته‌ی اصلی ممکن است در بعضی پروژه‌ها خالی باشد، پس با احتیاط می‌خوانیم
    let primaryIcon = "";
    let primaryName = "";
    let primaryId = null;

    if (project.primary_category_data) {
        primaryIcon = project.primary_category_data.icon || "";
        primaryName = project.primary_category_data.name || "";
        primaryId = project.primary_category_data.id;
    }

    // پیدا کردن یک دسته‌بندی دیگر (غیر از دسته‌ی اصلی) برای نمایش
    let otherCategoryName = "";
    const categoriesData = project.categories_data || [];
    for (let c = 0; c < categoriesData.length; c++) {
        if (categoriesData[c].id !== primaryId) {
            otherCategoryName = categoriesData[c].name || "";
            break; // اولین موردِ متفاوت کافی است
        }
    }

    // مقدارهای متنی که از API می‌آیند را با احتیاط برمی‌داریم
    const projectId = project.id;
    const status = project.status || "";
    const ownerName = project.display_owner_name || "";
    const title = project.title || "";

    // قیمت‌ها و سن پروژه عددی هستند، پس با Number امن می‌شوند
    const budgetMin = Number(project.budget_min).toLocaleString();
    const budgetMax = Number(project.budget_max).toLocaleString();
    const ageDays = project.project_age_days || "";

    // ── ۲) ساختن HTML کارت ──
    // هر مقداری که از API می‌آید و متن است با escapeHtml پاک می‌شود تا XSS رخ ندهد.
    return `
        <div class="card-project">

            <div class="card-top">

                <div class="icon-project">
                    <span>
                        <i class="${escapeHtml(primaryIcon)}"></i>
                    </span>
                </div>

                <div class="status-project">
                    <span class="active">${escapeHtml(status)}</span>
                </div>

                <label for="checkbox-${escapeHtml(projectId)}" class="bookmark">
                    <input
                        type="checkbox"
                        id="checkbox-${escapeHtml(projectId)}"
                        data-id="${escapeHtml(projectId)}"
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
                    ${escapeHtml(ownerName)}
                </h2>

                <h3>${escapeHtml(title)}</h3>

                <div class="card-pro-cat">
                    <p>${escapeHtml(primaryName)}</p>
                    <p>${escapeHtml(otherCategoryName)}</p>
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
    ${escapeHtml(ageDays)}
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
}