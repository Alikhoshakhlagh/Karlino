const form = document.getElementById('register-form');
const firstNameInput = document.getElementById('first-name');
const lastNameInput = document.getElementById('last-name');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const confirmPasswordInput = document.getElementById('confirm-password');
const submitBtn = document.querySelector('.submit');

const API_BASE = 'http://127.0.0.1:8000'; // ← آدرس سرور خودت رو بذار

// ── ترجمه ارورهای سرور به فارسی ──
function translateError(msg) {
    const map = {
        'user with this email already exists.': 'کاربری با این ایمیل قبلاً ثبت‌نام کرده است',
        'This field may not be blank.': 'این فیلد نمی‌تواند خالی باشد',
        'This field is required.': 'این فیلد الزامی است',
        'Enter a valid email address.': 'ایمیل معتبر وارد کنید',
        'Passwords do not match.': 'رمز عبور و تکرار آن یکسان نیستند',
        'This password is too short. It must contain at least 8 characters.': 'رمز باید حداقل ۸ کاراکتر باشد',
        'This password is too common.': 'این رمز عبور خیلی ساده است',
        'No active account found with the given credentials': 'ایمیل یا رمز عبور اشتباه است',
    };
    return map[msg] || msg; // اگه ترجمه نبود، همون متن اصلی رو برگردون
}

// ── نمایش ارور برای input های معمولی ──
function showError(inputEl, message) {
    inputEl.style.borderColor = '#ff4444';
    const label = inputEl.closest('label');
    let errorEl = label.querySelector('.error-msg');
    if (!errorEl) {
        errorEl = document.createElement('p');
        errorEl.className = 'error-msg';
        errorEl.style.cssText = 'color:#ff4444; font-size:12px; margin-top:4px;';
        label.appendChild(errorEl);
    }
    errorEl.textContent = message;
}

// ── پاک کردن ارور برای input های معمولی ──
function clearError(inputEl) {
    inputEl.style.borderColor = '';
    const label = inputEl.closest('label');
    const errorEl = label.querySelector('.error-msg');
    if (errorEl) errorEl.textContent = '';
}

// ── نمایش ارور برای gender ──
function showGenderError(message) {
    const genderOptions = document.querySelector('.gender-options');
    let errorEl = document.querySelector('.gender-error');
    if (!errorEl) {
        errorEl = document.createElement('p');
        errorEl.className = 'gender-error';
        errorEl.style.cssText = 'color:#ff4444; font-size:12px; margin-top:6px;';
        genderOptions.parentElement.appendChild(errorEl);
    }
    errorEl.textContent = message;
}

// ── پاک کردن ارور gender ──
function clearGenderError() {
    const errorEl = document.querySelector('.gender-error');
    if (errorEl) errorEl.textContent = '';
}

// ── نمایش ارور کلی فرم ──
function showFormError(message) {
    let errorEl = document.querySelector('.form-error');
    if (!errorEl) {
        errorEl = document.createElement('p');
        errorEl.className = 'form-error';
        errorEl.style.cssText = 'color:#ff4444; font-size:13px; margin-top:10px; text-align:center;';
        form.appendChild(errorEl);
    }
    errorEl.textContent = message;
}

// ── پاک کردن ارور کلی فرم ──
function clearFormError() {
    const errorEl = document.querySelector('.form-error');
    if (errorEl) errorEl.textContent = '';
}

// ── loading state دکمه ──
function setLoading(isLoading) {
    if (isLoading) {
        submitBtn.disabled = true;
        submitBtn.textContent = 'در حال ثبت‌نام...';
        submitBtn.style.opacity = '0.7';
        submitBtn.style.cursor = 'not-allowed';
    } else {
        submitBtn.disabled = false;
        submitBtn.textContent = 'ثبت‌نام';
        submitBtn.style.opacity = '1';
        submitBtn.style.cursor = 'pointer';
    }
}

// ── submit ──
form.addEventListener('submit', async function (e) {
    e.preventDefault();

    const firstName = firstNameInput.value.trim();
    const lastName = lastNameInput.value.trim();
    const email = emailInput.value.trim();
    const password = passwordInput.value;
    const confirmPassword = confirmPasswordInput.value;
    const selectedGender = document.querySelector('input[name="gender"]:checked');

    // پاک کردن ارورهای قبلی
    clearError(firstNameInput);
    clearError(lastNameInput);
    clearError(emailInput);
    clearError(passwordInput);
    clearError(confirmPasswordInput);
    clearGenderError();
    clearFormError();

    let hasError = false;

    if (firstName.length < 2) {
        showError(firstNameInput, 'نام باید حداقل ۲ کاراکتر باشد');
        hasError = true;
    }
    if (lastName.length < 2) {
        showError(lastNameInput, 'نام خانوادگی باید حداقل ۲ کاراکتر باشد');
        hasError = true;
    }
    if (!email.includes('@') || !email.includes('.')) {
        showError(emailInput, 'ایمیل معتبر نیست');
        hasError = true;
    }
    if (password.length < 8) {
        showError(passwordInput, 'رمز باید حداقل ۸ کاراکتر باشد');
        hasError = true;
    }
    if (password !== confirmPassword) {
        showError(confirmPasswordInput, 'رمز عبور و تکرار آن یکسان نیستند');
        hasError = true;
    }
    if (!selectedGender) {
        showGenderError('لطفاً جنسیت را انتخاب کنید');
        hasError = true;
    }

    if (hasError) return;

    const payload = {
        first_name: firstName,
        last_name: lastName,
        email: email,
        password: password,
        confirm_password: confirmPassword,
        gender: selectedGender.value, // باید 'male' یا 'female' باشد
    };

    setLoading(true);

    try {
        // ── مرحله ۱: ثبت‌نام ──
        const res = await fetch(`${API_BASE}/api/auth/register/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });

        const data = await res.json().catch(() => ({}));

        if (!res.ok) {
            // نمایش ارورهای برگشتی از سرور (با ترجمه فارسی)
            if (data.email) showError(emailInput, translateError(Array.isArray(data.email) ? data.email[0] : data.email));
            if (data.password) showError(passwordInput, translateError(Array.isArray(data.password) ? data.password[0] : data.password));
            if (data.first_name) showError(firstNameInput, translateError(Array.isArray(data.first_name) ? data.first_name[0] : data.first_name));
            if (data.last_name) showError(lastNameInput, translateError(Array.isArray(data.last_name) ? data.last_name[0] : data.last_name));
            if (data.confirm_password) showError(confirmPasswordInput, translateError(Array.isArray(data.confirm_password) ? data.confirm_password[0] : data.confirm_password));
            if (data.detail) showFormError(translateError(data.detail));
            if (!data.email && !data.password && !data.detail) {
                showFormError('ثبت‌نام ناموفق بود. دوباره تلاش کنید.');
            }
            setLoading(false);
            return;
        }

        // ── مرحله ۲: لاگین خودکار برای گرفتن توکن ──
        const loginRes = await fetch(`${API_BASE}/api/auth/login/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email, password: password }),
        });

        const loginData = await loginRes.json().catch(() => ({}));

        if (loginRes.ok && loginData.access) {
            // ذخیره توکن‌ها
            localStorage.setItem('access', loginData.access);
            localStorage.setItem('refresh', loginData.refresh);

            // ذخیره اطلاعات کاربر برای header (layout.js)
            localStorage.setItem('user', JSON.stringify({
                first_name: firstName,
                last_name: lastName,
                email: email,
                gender: selectedGender.value,
                isLoggedIn: true
            }));

            window.location.href = 'index.html';
        } else {
            // ثبت‌نام شد ولی لاگین خودکار نشد
            showFormError('ثبت‌نام انجام شد. لطفاً وارد شوید.');
            setLoading(false);
            // اگه خواستی به جای پیام، مستقیم بفرستش صفحه ورود:
            // window.location.href = 'login.html';
        }

    } catch (err) {
        showFormError('ارتباط با سرور برقرار نشد. اتصال اینترنت یا آدرس سرور را بررسی کنید.');
        setLoading(false);
    }
});