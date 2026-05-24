

const form = document.getElementById('register-form');
const firstNameInput = document.getElementById('first-name');
const lastNameInput = document.getElementById('last-name');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const confirmPasswordInput = document.getElementById('confirm-password');
const submitBtn = document.querySelector('.submit');

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

// ── نمایش ارور برای gender (جداست چون radio box ساختار فرق داره) ──
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
form.addEventListener('submit', function (e) {
    e.preventDefault();

    const firstName = firstNameInput.value.trim();
    const lastName = lastNameInput.value.trim();
    const email = emailInput.value.trim();
    const password = passwordInput.value;
    const confirmPassword = confirmPasswordInput.value;

    // گرفتن مقدار gender — null میشه اگه هیچکدام انتخاب نشده باشه
    const selectedGender = document.querySelector('input[name="gender"]:checked');

    // پاک کردن ارورهای قبلی
    clearError(firstNameInput);
    clearError(lastNameInput);
    clearError(emailInput);
    clearError(passwordInput);
    clearError(confirmPasswordInput);
    clearGenderError();

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

    // چک کردن gender
    if (!selectedGender) {
        showGenderError('لطفاً جنسیت را انتخاب کنید');
        hasError = true;
    }

    if (hasError) return;


    // اطلاعات کاربر
    const userData = {

        first_name: firstName,

        last_name: lastName,

        email: email,

        password: password,

        gender: selectedGender.value,

        isLoggedIn: true
    };


    // ذخیره در localStorage
    localStorage.setItem(
        'user',
        JSON.stringify(userData)
    );


    // loading
    setLoading(true);


    // redirect به صفحه اصلی
    setTimeout(function () {

        window.location.href = 'index.html';

    }, 1500);

});