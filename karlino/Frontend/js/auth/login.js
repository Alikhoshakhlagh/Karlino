const API_BASE = 'http://127.0.0.1:8000'; // ← آدرس سرور خودت رو بذار

const form = document.getElementById('login-form');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const submitBtn = document.querySelector('.submit');

// ── ترجمه ارورهای سرور به فارسی ──
function translateError(msg) {
    const map = {
        'No active account found with the given credentials': 'ایمیل یا رمز عبور اشتباه است',
        'This field may not be blank.': 'این فیلد نمی‌تواند خالی باشد',
        'This field is required.': 'این فیلد الزامی است',
        'Enter a valid email address.': 'ایمیل معتبر وارد کنید',
    };
    return map[msg] || msg;
}

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

function setLoading(isLoading) {
    if (isLoading) {
        submitBtn.disabled = true;
        submitBtn.textContent = 'در حال ورود...';
        submitBtn.style.opacity = '0.7';
    } else {
        submitBtn.disabled = false;
        submitBtn.textContent = 'ورود';
        submitBtn.style.opacity = '1';
    }
}

form.addEventListener('submit', async function (e) {
    e.preventDefault();

    const email = emailInput.value.trim();
    const password = passwordInput.value;

    clearError(emailInput);
    clearError(passwordInput);
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

    if (hasError) return;

    setLoading(true);

    try {
        const res = await fetch(`${API_BASE}/api/auth/login/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email, password: password }),
        });

        const data = await res.json().catch(() => ({}));

        if (res.ok && data.access) {
            // ورود موفق — ذخیره توکن‌ها
            localStorage.setItem('access', data.access);
            localStorage.setItem('refresh', data.refresh);

            // ذخیره اطلاعات کاربر برای header (layout.js)
            localStorage.setItem('user', JSON.stringify({
                email: email,
                isLoggedIn: true
            }));

            window.location.href = 'index.html';
        } else {
            // ورود ناموفق
            if (data.detail) {
                showFormError(translateError(data.detail));
            } else if (data.email) {
                showError(emailInput, translateError(Array.isArray(data.email) ? data.email[0] : data.email));
            } else if (data.password) {
                showError(passwordInput, translateError(Array.isArray(data.password) ? data.password[0] : data.password));
            } else {
                showFormError('ایمیل یا رمز عبور اشتباه است');
            }
            setLoading(false);
        }

    } catch (err) {
        showFormError('ارتباط با سرور برقرار نشد. اتصال اینترنت یا آدرس سرور را بررسی کنید.');
        setLoading(false);
    }
});