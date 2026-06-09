const API_BASE = 'http://localhost:8000'; // ← آدرس سرور خودت رو بذار

// ── گرفتن المنت‌ها ──
const form          = document.getElementById('forgot-form');
const emailInput    = document.getElementById('email');
const passwordInput = document.getElementById('password');
const confirmInput  = document.getElementById('confirm-password');
const submitBtn     = document.querySelector('.submit');

// ── ترجمه ارورهای سرور به فارسی ──
function translateError(msg) {
    const map = {
        'user with this email already exists.': 'کاربری با این ایمیل قبلاً ثبت‌نام کرده است',
        'This field may not be blank.': 'این فیلد نمی‌تواند خالی باشد',
        'This field is required.': 'این فیلد الزامی است',
        'Enter a valid email address.': 'ایمیل معتبر وارد کنید',
        'No active account found with the given credentials': 'حسابی با این مشخصات پیدا نشد',
        'User not found.': 'کاربری با این ایمیل پیدا نشد',
        'Not found.': 'کاربری با این ایمیل پیدا نشد',
    };
    return map[msg] || msg;
}

// ── نمایش ارور ──
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

// ── پاک کردن ارور ──
function clearError(inputEl) {
    inputEl.style.borderColor = '';
    const label = inputEl.closest('label');
    const errorEl = label.querySelector('.error-msg');
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

function clearFormError() {
    const errorEl = document.querySelector('.form-error');
    if (errorEl) errorEl.textContent = '';
}

// ── loading ──
function setLoading(isLoading) {
    if (isLoading) {
        submitBtn.disabled      = true;
        submitBtn.textContent   = 'در حال ذخیره...';
        submitBtn.style.opacity = '0.7';
    } else {
        submitBtn.disabled      = false;
        submitBtn.textContent   = 'ثبت رمز جدید';
        submitBtn.style.opacity = '1';
    }
}

// ── submit ──
form.addEventListener('submit', async function (e) {
    e.preventDefault();

    const email    = emailInput.value.trim();
    const password = passwordInput.value;
    const confirm  = confirmInput.value;

    clearError(emailInput);
    clearError(passwordInput);
    clearError(confirmInput);
    clearFormError();

    let hasError = false;

    if (!email.includes('@') || !email.includes('.')) {
        showError(emailInput, 'ایمیل معتبر نیست');
        hasError = true;
    }
    if (password.length < 8) {
        showError(passwordInput, 'رمز عبور باید حداقل ۸ کاراکتر باشد');
        hasError = true;
    }
    if (password !== confirm) {
        showError(confirmInput, 'رمز عبور و تکرار آن یکسان نیستند');
        hasError = true;
    }

    if (hasError) return;

    setLoading(true);

    try {
        const res = await fetch(`${API_BASE}/api/auth/forgot-password/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                email: email,
                new_password: password,
                confirm_password: confirm,
            }),
        });

        const data = await res.json().catch(() => ({}));

        if (res.ok) {
            setLoading(false);
            alert('رمز عبور با موفقیت تغییر کرد!');
            window.location.href = 'login.html';
        } else {
            if (data.email) showError(emailInput, translateError(Array.isArray(data.email) ? data.email[0] : data.email));
            if (data.new_password) showError(passwordInput, translateError(Array.isArray(data.new_password) ? data.new_password[0] : data.new_password));
            if (data.detail) showFormError(translateError(data.detail));
            if (!data.email && !data.new_password && !data.detail) {
                showFormError('تغییر رمز ناموفق بود. دوباره تلاش کنید.');
            }
            setLoading(false);
        }

    } catch (err) {
        showFormError('ارتباط با سرور برقرار نشد. اتصال اینترنت یا آدرس سرور را بررسی کنید.');
        setLoading(false);
    }
});