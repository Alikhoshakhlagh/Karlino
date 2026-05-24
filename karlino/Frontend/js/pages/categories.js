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

categories.slice(0, 10).forEach(category => {

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