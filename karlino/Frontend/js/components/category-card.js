function createCategoryCard(category) {
    const link = document.createElement("a");
    link.className = "cat-link";
    link.href =
        `projects.html?category=${encodeURIComponent(category.id)}`;

    const card = document.createElement("div");
    card.className = "card-Categories";

    const iconWrap = document.createElement("div");
    iconWrap.className = "icon-cat";

    const span = document.createElement("span");

    const icon = document.createElement("i");
    icon.className = category.icon;

    span.appendChild(icon);
    iconWrap.appendChild(span);

    const nameWrap = document.createElement("div");
    nameWrap.className = "name-cat";

    const name = document.createElement("p");
    name.textContent = category.name;

    nameWrap.appendChild(name);

    card.append(iconWrap, nameWrap);
    link.appendChild(card);

    return link;
}