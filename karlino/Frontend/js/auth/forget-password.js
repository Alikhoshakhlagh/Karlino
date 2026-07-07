const form = document.getElementById("forgot-form");

// جعبه‌های خطا (id ها دقیقاً مطابق HTML خودت)
const emailError = document.getElementById("error-email");
const passwordError = document.getElementById("error-password");
const confirmError = document.getElementById("error-confirmPassword"); // ← مطابق HTML تو
const formError = document.getElementById("error-form");

form.addEventListener("submit", async function (event) {

    event.preventDefault(); // جلوی رفرش صفحه

    // پاک‌کردن خطاهای قبلی
    emailError.textContent = "";
    passwordError.textContent = "";
    confirmError.textContent = "";
    formError.textContent = "";

    // خواندن مقادیر (.value تا متن را بگیرد، نه خود المنت)
    const email = document.getElementById("email").value;
    const newPassword = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirm-password").value;

    try {
        const response = await fetch(BASE_URL + ENDPOINTS.resetPassword, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            // اسم فیلدها طبق /api/docs/ خودت — درست هستند
            body: JSON.stringify({
                email: email,
                new_password: newPassword,
                confirm_password: confirmPassword
            })
        });

        const data = await response.json();

        // موفق → رمز عوض شد، برو صفحه‌ی ورود
        if (response.ok) {
            window.location.href = "login.html";
            return;
        }

        // ── خطاها از بک‌اند ──
        if (data.email) {
            emailError.textContent = data.email[0];

        }
        if (data.new_password) {
            passwordError.textContent = data.new_password[0];

        }
        if (data.confirm_password) {
            confirmError.textContent = data.confirm_password[0];

        }
        if (data.non_field_errors) {
            formError.textContent = data.non_field_errors[0];

        }
        if (data.detail) {
            formError.textContent = data.detail;

        }

    } catch (error) {
        // این حالت یعنی اصلاً به سرور وصل نشدیم، پس سرور هیچ پیامی نفرستاده
        // برای همین این یک پیام خودمان است، نه از بک‌اند
        document.getElementById("error-form").textContent = "ارتباط با سرور برقرار نشد";
    }

});