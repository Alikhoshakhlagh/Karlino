// ── load header ─────────────────────────────
fetch('./components/header.html')

    .then(response => response.text())

    .then(data => {

        document.getElementById('header-placeholder').innerHTML = data;

        initializeHeader();

    });


// ── load footer ─────────────────────────────
fetch('./components/footer.html')

    .then(response => response.text())

    .then(data => {

        document.getElementById('footer-placeholder').innerHTML = data;

    });


// ── مدیریت هدر ─────────────────────────────
function initializeHeader() {

    const guestHeader = document.querySelector('.guest-header');

    const userHeader = document.querySelector('.user-header');

    const logoutBtn = document.querySelector('.logout');


    const user = JSON.parse(
        localStorage.getItem('user')
    );


    // اگر لاگین بود
    if (user && user.isLoggedIn) {

        guestHeader.style.display = 'none';

        userHeader.style.display = 'flex';

    } else {

        guestHeader.style.display = 'flex';

        userHeader.style.display = 'none';
    }


    // logout
    if (logoutBtn) {

        logoutBtn.addEventListener('click', function () {

            localStorage.removeItem('user');

            window.location.reload();

        });

    }
    loadcategory_list();

}

async function loadcategory_list() {

    const list = document.getElementById("category-list");

    try {
        const data = await apiRequest(ENDPOINTS.categories);

        // اگه چیزی نبود
        if (!data.results || data.results.length === 0) {
            list.innerHTML = "<li>دسته‌بندی‌ای موجود نیست</li>";
            return;
        }

        list.innerHTML = "";

        for (let i = 0; i < data.results.length; i++) {
            const cat = data.results[i];

            const li = document.createElement("li");

            const a = document.createElement("a");
            // چون آدرس با متن ثابت "projects.html?..." شروع می‌شود، امن است
            a.href = "projects.html?category=" + cat.id;

            // اگر آیکون داشت، یک <i> بساز و کلاسش را ست کن
            if (cat.icon) {
                const icon = document.createElement("i");
                icon.className = cat.icon;
                a.appendChild(icon);
            }

            // نام دسته را به‌صورت متن خام اضافه کن (این خط، امن‌سازی اصلی است)
            a.appendChild(document.createTextNode(" " + cat.name));

            li.appendChild(a);
            list.appendChild(li);
        }

    } catch (err) {
        console.error("خطا در گرفتن دسته‌بندی‌ها:", err);
        list.innerHTML = "<li>خطا در بارگذاری</li>";
    }
}

