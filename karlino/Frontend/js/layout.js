// ── load header ─────────────────────────────
fetch('./components/header.html')

    .then(response => response.text())

    .then(data => {

        document.getElementById(
            'header-placeholder'
        ).innerHTML = data;

        initializeHeader();

    });


// ── load footer ─────────────────────────────
fetch('./components/footer.html')

    .then(response => response.text())

    .then(data => {

        document.getElementById(
            'footer-placeholder'
        ).innerHTML = data;

    });




// ── مدیریت هدر ─────────────────────────────
function initializeHeader() {

    const guestHeader =
        document.querySelector('.guest-header');

    const userHeader =
        document.querySelector('.user-header');

    const logoutBtn =
        document.querySelector('.logout');


    const user = JSON.parse(
        localStorage.getItem('user')
    );


    // اگر لاگین بود
    if (user && user.isLoggedIn) {

        guestHeader.style.display = 'none';

        userHeader.style.display = 'flex';

    } else {

        guestHeader.style.display = 'flex';

        userHeader.style.display = 'none';
    }


    // logout
    if (logoutBtn) {

        logoutBtn.addEventListener('click', function () {

            localStorage.removeItem('user');

            window.location.reload();

        });

    }

}