const form = document.getElementById("register-form");

// جعبه‌های خطا را یک‌بار می‌گیریم تا پایین راحت استفاده شوند
const firstnameError = document.getElementById("error-firstname");
const lastnameError = document.getElementById("error-lastname");
const emailError = document.getElementById("error-email");
const passwordError = document.getElementById("error-password");
const confirmPasswordError = document.getElementById("error-confirmPassword");
const genderError = document.getElementById("error-gender");
const formError = document.getElementById("error-form");

form.addEventListener("submit", async function (event) {

    event.preventDefault(); // جلوی رفرش صفحه

    // پاک‌کردن خطاهای قبلی: متن خالی + برداشتن کلاس show تا دوباره مخفی شوند
    firstnameError.textContent = "";
    lastnameError.textContent = "";
    emailError.textContent = "";
    passwordError.textContent = "";
    confirmPasswordError.textContent = "";
    genderError.textContent = "";
    formError.textContent = "";

    // خواندن مقادیری که کاربر تایپ کرده
    const firstName = document.getElementById("first-name").value;
    const lastName = document.getElementById("last-name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirm-password").value;

    // خواندن جنسیت انتخاب‌شده (اگر چیزی انتخاب نشده، خالی می‌ماند)
    const genderInput = document.querySelector('input[name="gender"]:checked');
    const gender = genderInput ? genderInput.value : "";

    try {
        // درخواست ثبت‌نام — همه‌ی فیلدها فرستاده می‌شوند
        const response = await fetch(BASE_URL + ENDPOINTS.register, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                first_name: firstName,
                last_name: lastName,
                email: email,
                password: password,
                confirm_password: confirmPassword,
                gender: gender
            })
        });

        // پاسخ سرور را می‌خوانیم
        const data = await response.json();

        if (response.ok) {
            window.location.href = "login.html";
            return;
        }

        // ── خطاهای فیلدی از بک‌اند (هر کدام آرایه است، [0] اولین پیام) ──

        if (data.first_name) {
            firstnameError.textContent = data.first_name[0];
        }
        if (data.last_name) {
            lastnameError.textContent = data.last_name[0];

        }
        if (data.email) {
            emailError.textContent = data.email[0];

        }
        if (data.password) {
            passwordError.textContent = data.password[0];

        }
        if (data.confirm_password) {
            confirmPasswordError.textContent = data.confirm_password[0];

        }
        if (data.gender) {
            genderError.textContent = data.gender[0];

        }

        // ── خطای کلی (بدون فیلد مشخص) ──
        if (data.non_field_errors) {
            formError.textContent = data.non_field_errors[0];
            formError.classList.add("show");
        }
        if (data.detail) {
            formError.textContent = data.detail;
            formError.classList.add("show");
        }

    } catch (error) {
        // سرور در دسترس نبود → پیام خودمان
        formError.textContent = "ارتباط با سرور برقرار نشد";
        formError.classList.add("show");
    }

});