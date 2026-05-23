// js/login.js


// ── گرفتن المنت‌ها ─────────────────────────────
const form = document.getElementById('login-form');

const emailInput = document.getElementById('email');

const passwordInput = document.getElementById('password');

const submitBtn = document.querySelector('.submit');


// ── نمایش ارور ─────────────────────────────
function showError(inputEl, message) {

    inputEl.style.borderColor = '#ff4444';

    const label = inputEl.closest('label');

    let errorEl = label.querySelector('.error-msg');

    if (!errorEl) {

        errorEl = document.createElement('p');

        errorEl.className = 'error-msg';

        errorEl.style.cssText = `
            color:#ff4444;
            font-size:12px;
            margin-top:4px;
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

        submitBtn.disabled = true;

        submitBtn.textContent = 'در حال ورود...';

        submitBtn.style.opacity = '0.7';

    } else {

        submitBtn.disabled = false;

        submitBtn.textContent = 'ورود';

        submitBtn.style.opacity = '1';
    }
}


// ── submit ─────────────────────────────
form.addEventListener('submit', function (e) {

    e.preventDefault();


    const email = emailInput.value.trim();

    const password = passwordInput.value;


    // پاک کردن ارورها
    clearError(emailInput);

    clearError(passwordInput);


    let hasError = false;


    // validation ایمیل
    if (!email.includes('@') || !email.includes('.')) {

        showError(
            emailInput,
            'ایمیل معتبر نیست'
        );

        hasError = true;
    }


    // validation رمز
    if (password.length < 8) {

        showError(
            passwordInput,
            'رمز عبور باید حداقل ۸ کاراکتر باشد'
        );

        hasError = true;
    }


    if (hasError) return;


    // گرفتن کاربر ذخیره شده
    const savedUser = JSON.parse(
        localStorage.getItem('user')
    );


    // چک وجود کاربر
    if (!savedUser) {

        showError(
            emailInput,
            'حساب کاربری پیدا نشد'
        );

        return;
    }


    // چک ایمیل
    if (savedUser.email !== email) {

        showError(
            emailInput,
            'ایمیل اشتباه است'
        );

        return;
    }


    // چک رمز
    if (savedUser.password !== password) {

        showError(
            passwordInput,
            'رمز عبور اشتباه است'
        );

        return;
    }


    // لاگین موفق
    savedUser.isLoggedIn = true;


    // ذخیره دوباره
    localStorage.setItem(
        'user',
        JSON.stringify(savedUser)
    );


    // loading
    setLoading(true);


    // redirect
    setTimeout(function () {

        window.location.href = 'index.html';

    }, 1500);

});