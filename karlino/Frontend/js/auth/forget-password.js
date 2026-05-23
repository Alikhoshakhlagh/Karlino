// ── گرفتن المنت‌ها ─────────────────────────────
const form            = document.getElementById('forgot-form');
const emailInput      = document.getElementById('email');
const passwordInput   = document.getElementById('password');
const confirmInput    = document.getElementById('confirm-password');
const submitBtn       = document.querySelector('.submit');


// ── نمایش ارور ─────────────────────────────
function showError(inputEl, message) {

    inputEl.style.borderColor = '#ff4444';

    const label = inputEl.closest('label');

    let errorEl = label.querySelector('.error-msg');

    if (!errorEl) {

        errorEl = document.createElement('p');

        errorEl.className = 'error-msg';

        errorEl.style.cssText = `
            color: #ff4444;
            font-size: 12px;
            margin-top: 4px;
        `;

        label.appendChild(errorEl);
    }

    errorEl.textContent = message;
}


// ── پاک کردن ارور ─────────────────────────────
function clearError(inputEl) {

    inputEl.style.borderColor = '';

    const label = inputEl.closest('label');

    const errorEl = label.querySelector('.error-msg');

    if (errorEl) {
        errorEl.textContent = '';
    }
}


// ── loading ─────────────────────────────
function setLoading(isLoading) {

    if (isLoading) {

        submitBtn.disabled    = true;
        submitBtn.textContent = 'در حال ذخیره...';
        submitBtn.style.opacity = '0.7';

    } else {

        submitBtn.disabled    = false;
        submitBtn.textContent = 'ثبت رمز جدید';
        submitBtn.style.opacity = '1';
    }
}


// ── submit ─────────────────────────────
form.addEventListener('submit', function (e) {

    e.preventDefault();

    const email    = emailInput.value.trim();
    const password = passwordInput.value;
    const confirm  = confirmInput.value;

    // پاک کردن ارورهای قبلی
    clearError(emailInput);
    clearError(passwordInput);
    clearError(confirmInput);

    let hasError = false;


    // ── validation ایمیل ──────────────
    if (!email.includes('@') || !email.includes('.')) {

        showError(emailInput, 'ایمیل معتبر نیست');
        hasError = true;
    }


    // ── validation رمز جدید ──────────────
    if (password.length < 6) {

        showError(passwordInput, 'رمز عبور باید حداقل ۶ کاراکتر باشد');
        hasError = true;
    }


    // ── چک تطابق رمزها ──────────────
    if (password !== confirm) {

        showError(confirmInput, 'رمز عبور و تکرار آن یکسان نیستند');
        hasError = true;
    }


    if (hasError) return;


    // ── چک وجود حساب در localStorage ──────────────
    const savedUser = JSON.parse(localStorage.getItem('user'));

    if (!savedUser) {

        showError(emailInput, 'حساب کاربری پیدا نشد');
        return;
    }

    if (savedUser.email !== email) {

        showError(emailInput, 'ایمیلی با این حساب وجود ندارد');
        return;
    }


    // ── ذخیره رمز جدید ──────────────
    setLoading(true);

    setTimeout(function () {

        savedUser.password = password;

        localStorage.setItem('user', JSON.stringify(savedUser));

        setLoading(false);

        // نمایش پیام موفقیت و redirect به login
        alert('رمز عبور با موفقیت تغییر کرد!');

        window.location.href = 'login.html';

    }, 1000);

});