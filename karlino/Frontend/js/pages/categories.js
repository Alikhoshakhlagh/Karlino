const categoriesContainer = document.getElementById("categoriesContainer");
const paginationContainer = document.querySelector(".category-pagination");

const PAGE_SIZE = 20;       // تعداد کارت در هر صفحه
let currentPage = 1;        // صفحه‌ی فعلی
let allCategories = [];      // همه‌ی دسته‌بندی‌ها را یک‌بار از سرور می‌گیریم

// ── گرفتن «همه‌ی» دسته‌بندی‌ها از همه‌ی صفحه‌های سرور ──
async function fetchAllCategories() {
    let all = [];
    let url = BASE_URL + ENDPOINTS.categories;

    // تا وقتی صفحه‌ی بعدی وجود دارد، ادامه بده
    while (url) {
        const response = await fetch(url);
        if (!response.ok) throw new Error("خطا در دریافت اطلاعات");

        const data = await response.json();
        all = all.concat(data.results); // نتایج این صفحه را اضافه کن
        url = data.next;                // لینک صفحه‌ی بعد، یا null اگر تمام شد
    }

    return all;
}

// ── نمایش یک صفحه‌ی مشخص ──
function renderPage(page) {
    currentPage = page;

    // برش ۲۰تایی: از کجا تا کجا
    const start = (page - 1) * PAGE_SIZE;
    const end = start + PAGE_SIZE;
    const pageItems = allCategories.slice(start, end);

    // کارت‌های این صفحه را بساز
    categoriesContainer.innerHTML = "";
    pageItems.forEach((category) => {
        categoriesContainer.innerHTML += `
<a class="cat-link" href="projects.html?category=${category.id}">
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

    renderPagination();      // دکمه‌های صفحه را به‌روز کن
    window.scrollTo(0, 0);   // برو بالای صفحه
}

// ── ساختن دکمه‌های صفحه‌بندی ──
function renderPagination() {
    const totalPages = Math.ceil(allCategories.length / PAGE_SIZE);

    paginationContainer.innerHTML = "";

    // اگر فقط یک صفحه باشد، دکمه‌ای لازم نیست
    if (totalPages <= 1) return;

    for (let i = 1; i <= totalPages; i++) {
        const button = document.createElement("button");
        button.className = "page-btn";
        if (i === currentPage) button.classList.add("active"); // صفحه‌ی فعلی
        button.textContent = i;

        // با کلیک، همان صفحه را نشان بده
        button.addEventListener("click", function () {
            renderPage(i);
        });

        paginationContainer.appendChild(button);
    }
}

// ── شروع ──
async function loadCategories() {
    categoriesContainer.innerHTML = "<p>در حال بارگذاری...</p>";

    try {
        allCategories = await fetchAllCategories();

        if (allCategories.length === 0) {
            categoriesContainer.innerHTML = "<p>دسته‌بندی‌ای موجود نیست.</p>";
            return;
        }

        renderPage(1); // صفحه‌ی اول را نشان بده

    } catch (error) {
        console.error("خطا در دریافت دسته‌بندی‌ها:", error);
        categoriesContainer.innerHTML =
            "<p class='field-error'>خطا در دریافت دسته‌بندی‌ها.</p>";
    }
}

loadCategories();