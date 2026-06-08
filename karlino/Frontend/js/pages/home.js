const categories = [
    {
        title: "توسعه وب",
        projects: "12,500+",
        icon: "fa-solid fa-code"
    },

    {
        title: "UI/UX Design",
        projects: "8,200+",
        icon: "fa-solid fa-pen-ruler"
    },
    {
        title: "امنیت شبکه",
        projects: "2,100+",
        icon: "fa-solid fa-shield-halved"
    },

    {
        title: "هوش مصنوعی",
        projects: "5,100+",
        icon: "fa-solid fa-robot"
    },

    {
        title: "Graphic Design",
        projects: "6,500+",
        icon: "fa-solid fa-palette"
    },

    {
        title: "تولید محتوا",
        projects: "5,900+",
        icon: "fa-solid fa-video"
    },

    {
        title: "دیجیتال مارکتینگ",
        projects: "7,400+",
        icon: "fa-solid fa-bullhorn"
    },

    {
        title: "برنامه نویسی موبایل",
        projects: "4,800+",
        icon: "fa-solid fa-mobile-screen"
    },

    {
        title: "سئو و بهینه سازی",
        projects: "3,700+",
        icon: "fa-solid fa-chart-line"
    },

    {
        title: "ویرایش ویدیو",
        projects: "4,300+",
        icon: "fa-solid fa-film"
    },

    {
        title: "ترجمه و زبان",
        projects: "2,900+",
        icon: "fa-solid fa-language"
    },

    {
        title: "ورود داده و تایپ",
        projects: "3,200+",
        icon: "fa-solid fa-keyboard"
    }
];

const container = document.getElementById("categoriesContainer");

categories.slice(0, 9).forEach(category => {

    container.innerHTML += `

        <div class="card-Categories">

            <div class="icon-cat">
                <span>
                    <i class="${category.icon}"></i>
                </span>
            </div>

            <div class="name-cat">
                <p>${category.title}</p>
            </div>

            <div class="project-stats">
                <h3 class="count">${category.projects}</h3>
                <p class="lable">پروژه</p>
            </div>

        </div>

    `;

});

const projects = [
    {
        owner: "نیلوفر زمانی",
        title: "تدوین ویدیو اینستاگرام",
        categories: ["تدوین ویدیو", "شبکه اجتماعی"],
        price: "7,000 - 4,500",
        daysAgo: "3 روز پیش",
        icon: "fa-solid fa-video"
    },

    {
        owner: "پارسا نیکخواه",
        title: "طراحی داشبورد مدیریتی",
        categories: ["UI/UX", "طراحی وب"],
        price: "15,000 - 10,000",
        daysAgo: "6 روز پیش",
        icon: "fa-solid fa-chart-line"
    },

    {
        owner: "ریحانه موسوی",
        title: "تولید محتوای بلاگ",
        categories: ["تولید محتوا", "SEO"],
        price: "6,000 - 3,500",
        daysAgo: "4 روز پیش",
        icon: "fa-solid fa-pen"
    },

    {
        owner: "آرین شریفی",
        title: "طراحی بنر تبلیغاتی",
        categories: ["طراحی گرافیک", "تبلیغات"],
        price: "3,500 - 1,500",
        daysAgo: "9 روز پیش",
        icon: "fa-solid fa-image"
    },

    {
        owner: "مبینا اسدی",
        title: "طراحی اپلیکیشن فروشگاهی",
        categories: ["Mobile App", "UI Design"],
        price: "18,000 - 12,000",
        daysAgo: "1 روز پیش",
        icon: "fa-solid fa-mobile"
    },

    {
        owner: "عرفان تهرانی",
        title: "پیاده سازی پنل ادمین",
        categories: ["توسعه وب", "React"],
        price: "14,000 - 9,000",
        daysAgo: "7 روز پیش",
        icon: "fa-solid fa-laptop-code"
    },

    {
        owner: "هلیا رستگار",
        title: "طراحی کارت ویزیت حرفه‌ای",
        categories: ["چاپ", "برندینگ"],
        price: "2,500 - 1,000",
        daysAgo: "2 روز پیش",
        icon: "fa-solid fa-id-card"
    },

    {
        owner: "کیان مرادی",
        title: "ساخت موشن گرافیک تبلیغاتی",
        categories: ["موشن گرافیک", "تبلیغات"],
        price: "11,000 - 7,500",
        daysAgo: "10 روز پیش",
        icon: "fa-solid fa-film"
    },

    {
        owner: "شایان اکبری",
        title: "بهینه سازی سئو سایت",
        categories: ["SEO", "دیجیتال مارکتینگ"],
        price: "9,500 - 5,000",
        daysAgo: "5 روز پیش",
        icon: "fa-solid fa-magnifying-glass-chart"
    },

    {
        owner: "ترانه حیدری",
        title: "طراحی لندینگ پیج محصول",
        categories: ["Landing Page", "UI/UX"],
        price: "13,000 - 8,500",
        daysAgo: "امروز",
        icon: "fa-solid fa-window-maximize"
    },
];

const projectsContainer = document.getElementById("projectsContainer");

projectsContainer.innerHTML = "";

projects.slice(0, 8).forEach((project, index) => {

    projectsContainer.innerHTML += `

    <div class="card-project">

        <div class="card-top">

            <div class="icon-project">
                <span>
                    <i class="${project.icon}"></i>
                </span>
            </div>
<div class="status-project">
                    <span class="active">فعال</span>
            </div>
            <label for="checkbox-${index}" class="bookmark">

                <input 
                    type="checkbox" 
                    id="checkbox-${index}"
                />

                <svg
                    width="15"
                    viewBox="0 0 50 70"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                    class="svgIcon"
                >
                    <path
                        d="M46 62.0085L46 3.88139L3.99609 3.88139L3.99609 62.0085L24.5 45.5L46 62.0085Z"
                        stroke="black"
                        stroke-width="7"
                    ></path>
                </svg>

            </label>
            
        </div>

        <div class="card-content">

            <h2 class="owner">
                <i class="fa-solid fa-user"></i>
                ${project.owner}
            </h2>

            <h3>${project.title}</h3>

            <div class="card-pro-cat">

                ${project.categories.map(category => `
                
                    <p class="categori">
                        ${category}
                    </p>

                `).join("")}

            </div>

            <div class="price">
                <span>تومان</span>
                <span class="number">${project.price}</span>
            </div>

        </div>

        <div class="card-footer">

            <span class="daysAgo">
                ${project.daysAgo}
            </span>

            <button class="button" type="button">

                <div class="button-box">

                    <span class="button-elem">

                        <svg viewBox="0 0 46 40" xmlns="http://www.w3.org/2000/svg">

                            <path
                                d="M46 20.038c0-.7-.3-1.5-.8-2.1l-16-17c-1.1-1-3.2-1.4-4.4-.3-1.2 1.1-1.2 3.3 0 4.4l11.3 11.9H3c-1.7 0-3 1.3-3 3s1.3 3 3 3h33.1l-11.3 11.9c-1 1-1.2 3.3 0 4.4 1.2 1.1 3.3.8 4.4-.3l16-17c.5-.5.8-1.1.8-1.9z"
                            ></path>

                        </svg>

                    </span>

                    <span class="button-elem">

                        <svg viewBox="0 0 46 40">

                            <path
                                d="M46 20.038c0-.7-.3-1.5-.8-2.1l-16-17c-1.1-1-3.2-1.4-4.4-.3-1.2 1.1-1.2 3.3 0 4.4l11.3 11.9H3c-1.7 0-3 1.3-3 3s1.3 3 3 3h33.1l-11.3 11.9c-1 1-1.2 3.3 0 4.4 1.2 1.1 3.3.8 4.4-.3l16-17c.5-.5.8-1.1.8-1.9z"
                            ></path>

                        </svg>

                    </span>

                </div>

            </button>

        </div>

    </div>

    `;
});