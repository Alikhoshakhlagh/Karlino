

// ─── Sort Box ───────────────────────────────────────────────
const selectedOption = document.querySelector(".selected-option");
const optionsContainer = document.querySelector(".options-container");
const options = document.querySelectorAll(".option");

selectedOption.addEventListener("click", (e) => {
    e.stopPropagation(); // جلوگیری از bubble شدن به document
    optionsContainer.classList.toggle("show");
});

options.forEach(option => {
    option.addEventListener("click", () => {
        selectedOption.innerHTML = `
            ${option.innerText}
            <i class="fa-solid fa-angle-down"></i>
        `;
        optionsContainer.classList.remove("show");
    });
});

// بسته شدن با کلیک بیرون از باکس
document.addEventListener("click", (e) => {
    if (!e.target.closest(".sort-box")) {
        optionsContainer.classList.remove("show");
    }
});

///////pagination
const pageButtons =
    document.querySelectorAll(".page-btn");


pageButtons.forEach(button => {

    button.addEventListener("click", () => {

        if (
            button.classList.contains("arrow-btn")
        ) {
            return;
        }


        document
            .querySelector(".page-btn.active")
            ?.classList.remove("active");


        button.classList.add("active");

    });

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
    }

];


/*
برای تست:
پروژه‌ها را زیاد میکنیم
تا 20 کارت ساخته شود
*/

const fakeProjects = [];


for (let i = 0; i < 9; i++) {

    fakeProjects.push(
        projects[i % projects.length]
    );

}


const projectsContainer =
    document.getElementById(
        "projectsContainer"
    );


projectsContainer.innerHTML = "";


fakeProjects.forEach((project, index) => {

    projectsContainer.innerHTML += `

         <div class="card-project">

        <div class="card-top">

            <div class="icon-project">
                <span>
                    <i class="${project.icon}"></i>
                </span>
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

// ─── Clear Filter ────────────────────────────────────────────
const clearFilterBtn = document.querySelector(".clear-filter");

clearFilterBtn.addEventListener("click", () => {
    document.querySelectorAll(".items-container input[type='checkbox']").forEach(checkbox => {
        checkbox.checked = false;
    });
});

