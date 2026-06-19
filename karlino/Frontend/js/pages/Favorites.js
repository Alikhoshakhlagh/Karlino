// ===== favorites.js — منطق مشترک علاقه‌مندی‌ها =====
// مهم: این فایل باید «قبل از» home.js و projects.js لود شود

const FAV_BASE = "http://127.0.0.1:8000";

// ── گرفتن id پروژه‌هایی که کاربر علاقه‌مند کرده ──
async function getFavoriteIds() {
    const token = localStorage.getItem("access");
    if (!token) return []; // لاگین نیست → لیست خالی

    try {
        const response = await fetch(`${FAV_BASE}/api/favorites/`, {
            headers: { "Authorization": "Bearer " + token }
        });
        if (!response.ok) return [];

        const data = await response.json();
        // ممکن است آرایه‌ی ساده باشد یا صفحه‌بندی‌شده (results)
        const favorites = Array.isArray(data) ? data : (data.results || []);

        // فقط id پروژه‌ها را برمی‌گردانیم
        return favorites.map(fav => fav.project);
    } catch (error) {
        console.error("خطا در گرفتن علاقه‌مندی‌ها:", error);
        return [];
    }
}

// ── تیک‌زدن چک‌باکس‌های علاقه‌مندیِ قبلی (حفظ وضعیت بعد از رفرش) ──
async function markFavorites() {
    const favoriteIds = await getFavoriteIds();

    const checkboxes = document.querySelectorAll(".bookmark input[type='checkbox']");
    checkboxes.forEach(checkbox => {
        // اگر id این پروژه در لیست علاقه‌مندی‌ها بود، تیکش بزن
        if (favoriteIds.includes(checkbox.dataset.id)) {
            checkbox.checked = true;
        }
    });
}

// ── خاموش/روشن‌کردن یک علاقه‌مندی در سرور ──
async function toggleFavorite(projectId) {
    const token = localStorage.getItem("access");

    // اگر کاربر لاگین نکرده، بفرستش به صفحه‌ی ورود
    if (!token) {
        window.location.href = "login.html";
        return;
    }

    try {
        const response = await fetch(`${FAV_BASE}/api/favorites/${projectId}/toggle/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token // ← توکن کاربر
            }
        });
        if (!response.ok) {
            console.error("خطا در ذخیره‌ی علاقه‌مندی. وضعیت:", response.status);
        }
    } catch (error) {
        console.error("خطا:", error);
    }
}

// ── گوش‌دادن به کلیک هر چک‌باکس ──
function attachBookmarkListeners() {
    const checkboxes = document.querySelectorAll(".bookmark input[type='checkbox']");
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener("change", function () {
            toggleFavorite(checkbox.dataset.id);
        });
    });
}

// ── این را بعد از ساختن کارت‌ها در هر صفحه صدا بزن ──
async function initBookmarks() {
    attachBookmarkListeners(); // به کلیک‌ها گوش بده
    await markFavorites();     // علاقه‌مندی‌های قبلی را تیک بزن
}