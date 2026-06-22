// المنت فرم را می‌گیریم
const form = document.getElementById("login-form");

// وقتی فرم ارسال شد، این کد اجرا می‌شود
form.addEventListener("submit", async function (event) {

    event.preventDefault(); // جلوی رفرش‌شدن خودکار صفحه را می‌گیرد

    // پاک‌کردن خطاهای دفعه‌ی قبل
    document.getElementById("error-email").textContent = "";
    document.getElementById("error-password").textContent = "";
    document.getElementById("error-form").textContent = "";

    // خواندن مقادیری که کاربر تایپ کرده
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
        // درخواست ورود را به سرور می‌فرستیم
        const response = await fetch(BASE_URL + ENDPOINTS.login, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: email, password: password })
        });

        // پاسخ سرور را می‌خوانیم
        const data = await response.json();

        // اگر ورود موفق بود
        if (response.ok) {
            localStorage.setItem("access", data.access);
            localStorage.setItem("refresh", data.refresh);
            localStorage.setItem("user", JSON.stringify({ email: email, isLoggedIn: true }));
            window.location.href = "index.html";
            return;
        }

        // اگر سرور درباره‌ی فیلد ایمیل خطا داد، همان پیام سرور را نشان بده
        if (data.email) {
            document.getElementById("error-email").textContent = data.email[0];
        }

        // اگر سرور درباره‌ی فیلد رمز خطا داد، همان پیام سرور را نشان بده
        if (data.password) {
            document.getElementById("error-password").textContent = data.password[0];
        }

        // اگر سرور خطای کلی داد (ایمیل یا رمز اشتباه)، همان پیام سرور را نشان بده
        if (data.detail) {
            document.getElementById("error-form").textContent = data.detail;
        }

    } catch (error) {
        // این حالت یعنی اصلاً به سرور وصل نشدیم، پس سرور هیچ پیامی نفرستاده
        // برای همین این یک پیام خودمان است، نه از بک‌اند
        document.getElementById("error-form").textContent = "ارتباط با سرور برقرار نشد";
    }

});