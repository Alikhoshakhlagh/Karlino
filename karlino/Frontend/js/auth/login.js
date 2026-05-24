const fakeUsers = [
    {
        first_name: 'علی',
        last_name: 'رضایی',
        email: 'ali.rezaei@gmail.com',
        password: 'Ali@12345',
        gender: 'male',
        isLoggedIn: false
    },
    {
        first_name: 'سارا',
        last_name: 'محمدی',
        email: 'sara.mohammadi@yahoo.com',
        password: 'Sara#2024',
        gender: 'female',
        isLoggedIn: false
    },
    {
        first_name: 'محمد',
        last_name: 'حسینی',
        email: 'm.hosseini@outlook.com',
        password: 'Mhmd@5678',
        gender: 'male',
        isLoggedIn: false
    }
];

if (!localStorage.getItem('user')) {
    localStorage.setItem('user', JSON.stringify(fakeUsers[0]));
}


const form = document.getElementById('login-form');

const emailInput = document.getElementById('email');

const passwordInput = document.getElementById('password');

const submitBtn = document.querySelector('.submit');



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


function clearError(inputEl) {

    inputEl.style.borderColor = '';

    const label = inputEl.closest('label');

    const errorEl = label.querySelector('.error-msg');

    if (errorEl) {
        errorEl.textContent = '';
    }
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


form.addEventListener('submit', function (e) {

    e.preventDefault();

    const email = emailInput.value.trim();

    const password = passwordInput.value;

    clearError(emailInput);

    clearError(passwordInput);

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

    const savedUser = JSON.parse(localStorage.getItem('user'));

    if (!savedUser) {

        showError(emailInput, 'حساب کاربری پیدا نشد');

        return;
    }

    if (savedUser.email !== email) {

        showError(emailInput, 'ایمیل اشتباه است');

        return;
    }

    if (savedUser.password !== password) {

        showError(passwordInput, 'رمز عبور اشتباه است');

        return;
    }

    savedUser.isLoggedIn = true;

    localStorage.setItem('user', JSON.stringify(savedUser));

    setLoading(true);

    setTimeout(function () {

        window.location.href = 'index.html';

    }, 1500);

});