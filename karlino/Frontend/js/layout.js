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

    const list = document.getElementById("category-list")

    try {
        const data = await apiRequest(ENDPOINTS.categories);

        // اگه چیزی نبود
        if (!data.results || data.results.length === 0) {
            list.innerHTML = "<li>دسته‌بندی‌ای موجود نیست</li>";
            return;
        }
        list.innerHTML = "";
        data.results.forEach((cat) => {
            const li = document.createElement("li");
            li.innerHTML = `
        <a href="projects.html?category=${cat.id}">
          ${cat.icon ? `<i class="${cat.icon}"></i>` : ""}
          ${cat.name}
        </a>`;
            list.appendChild(li);
        });
    } catch (err) {
        console.error("خطا در گرفتن دسته‌بندی‌ها:", err);
        list.innerHTML = "<li>خطا در بارگذاری</li>";
    }
}


