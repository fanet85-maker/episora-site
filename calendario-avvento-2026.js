(function () {
    const calendar = document.querySelector(".calendar");
    if (!calendar) return;

    const translations = {
        it: {
            open: "Apri la finestra",
            locked: "Si apre quando il film è pubblicato",
            title: "Film in arrivo",
            description: "La scheda del film verrà pubblicata qui.",
            add: "Aggiungi il film all’app",
            instagram: "Guarda il post su Instagram"
        },
        en: {
            open: "Open the window",
            locked: "Opens when the movie is published",
            title: "Movie coming soon",
            description: "The movie details will be published here.",
            add: "Add the movie to the app",
            instagram: "View the Instagram post"
        },
        es: {
            open: "Abrir la ventana",
            locked: "Se abre al publicarse la película",
            title: "Película próximamente",
            description: "Aquí se publicarán los detalles de la película.",
            add: "Añadir la película a la app",
            instagram: "Ver la publicación en Instagram"
        },
        fr: {
            open: "Ouvrir la fenêtre",
            locked: "S’ouvre à la publication du film",
            title: "Film bientôt disponible",
            description: "Les détails du film seront publiés ici.",
            add: "Ajouter le film à l’application",
            instagram: "Voir la publication Instagram"
        },
        de: {
            open: "Fenster öffnen",
            locked: "Öffnet sich mit der Veröffentlichung des Films",
            title: "Film folgt bald",
            description: "Die Filmdetails werden hier veröffentlicht.",
            add: "Film zur App hinzufügen",
            instagram: "Instagram-Beitrag ansehen"
        },
        ru: {
            open: "Открыть окно",
            locked: "Откроется после публикации фильма",
            title: "Фильм скоро появится",
            description: "Информация о фильме появится здесь.",
            add: "Добавить фильм в приложение",
            instagram: "Смотреть публикацию в Instagram"
        }
    };

    const language = document.documentElement.lang.slice(0, 2).toLowerCase();
    const text = translations[language];
    if (!text) {
        throw new Error("Missing Advent calendar translation for " + language);
    }

    const storageKey = "episora-advent-calendar-2026-opened";
    const savedDays = window.localStorage.getItem(storageKey);
    let openedDays = new Set();
    if (savedDays) {
        let parsedDays;
        try {
            parsedDays = JSON.parse(savedDays);
        } catch (error) {
            throw new Error("Could not read the saved Advent calendar state", { cause: error });
        }
        if (!Array.isArray(parsedDays) || parsedDays.some((day) => typeof day !== "string")) {
            throw new Error("Saved Advent calendar state has an invalid format");
        }
        openedDays = new Set(parsedDays);
    }

    function safeHttpsUrl(value) {
        if (!value) return null;
        const url = new URL(value, window.location.href);
        if (url.protocol !== "https:") {
            throw new Error("Advent calendar links must use HTTPS");
        }
        return url.href;
    }

    const doors = Array.from(calendar.querySelectorAll(".day"), (day, index) => {
        const date = day.querySelector("time");
        const teaser = day.querySelector(".locked");
        if (!date || !teaser) {
            throw new Error("Advent calendar day is missing its date or teaser");
        }

        const number = date.dateTime.slice(-2).replace(/^0/, "");
        const detailId = `advent-movie-${index + 1}`;
        const door = document.createElement("button");
        door.className = "day__door";
        door.type = "button";
        door.setAttribute("aria-expanded", "false");
        door.setAttribute("aria-controls", detailId);

        const leftShutter = document.createElement("span");
        leftShutter.className = "day__shutter day__shutter--left";
        leftShutter.setAttribute("aria-hidden", "true");

        const rightShutter = document.createElement("span");
        rightShutter.className = "day__shutter day__shutter--right";
        rightShutter.setAttribute("aria-hidden", "true");

        const snow = document.createElement("span");
        snow.className = "day__snow";
        snow.setAttribute("aria-hidden", "true");

        const garland = document.createElement("span");
        garland.className = "day__garland";
        garland.setAttribute("aria-hidden", "true");

        const bulbColors = ["#ffcf70", "#f78a83", "#b9e6ae", "#c4b5fd", "#ffcf70", "#b9e6ae", "#f78a83", "#ffcf70"];
        bulbColors.forEach((color, bulbIndex) => {
            const bulb = document.createElement("span");
            bulb.className = "day__bulb";
            bulb.style.setProperty("--bulb-color", color);
            bulb.style.setProperty("--bulb-delay", `${bulbIndex * -0.31}s`);
            bulb.style.left = `${5 + bulbIndex * 13}%`;
            bulb.style.top = `${bulbIndex % 2 === 0 ? 2 : 8}px`;
            garland.append(bulb);
        });

        const filmstrip = document.createElement("span");
        filmstrip.className = "day__filmstrip";
        filmstrip.setAttribute("aria-hidden", "true");

        const dayNumber = document.createElement("span");
        dayNumber.className = "day__number";
        dayNumber.textContent = number;

        const doorLabel = document.createElement("span");
        doorLabel.className = "day__door-label";
        door.append(leftShutter, rightShutter, snow, garland, filmstrip, dayNumber, doorLabel);

        const content = document.createElement("div");
        content.className = "day__content";
        content.id = detailId;
        content.hidden = true;
        content.tabIndex = -1;

        const contentDate = date.cloneNode(true);
        const title = document.createElement("h3");
        title.id = `${detailId}-title`;
        title.textContent = day.dataset.movieTitle?.trim() || text.title;

        const description = document.createElement("p");
        description.textContent = day.dataset.movieDescription?.trim() || text.description;

        const links = document.createElement("div");
        links.className = "day__links";

        const appUrl = safeHttpsUrl(day.dataset.appUrl);
        if (appUrl) {
            const addLink = document.createElement("a");
            addLink.href = appUrl;
            addLink.textContent = text.add;
            links.append(addLink);
        }

        const instagramUrl = safeHttpsUrl(day.dataset.instagramUrl);
        if (instagramUrl) {
            const instagramLink = document.createElement("a");
            instagramLink.href = instagramUrl;
            instagramLink.textContent = text.instagram;
            instagramLink.target = "_blank";
            instagramLink.rel = "noopener noreferrer";
            links.append(instagramLink);
        }

        content.setAttribute("aria-labelledby", title.id);
        content.append(contentDate, title, description);
        if (links.childElementCount > 0) content.append(links);

        day.replaceChildren(content, door);

        function openDoor(restore = false) {
            content.hidden = false;
            door.setAttribute("aria-expanded", "true");
            door.setAttribute("aria-hidden", "true");
            door.tabIndex = -1;
            day.classList.add("is-open");
            if (restore || window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
                door.hidden = true;
                if (restore) return;
            }
            content.focus({ preventScroll: true });
        }

        door.addEventListener("click", () => {
            openedDays.add(date.dateTime);
            window.localStorage.setItem(storageKey, JSON.stringify(Array.from(openedDays)));
            openDoor();
        });

        const shutters = new Set([leftShutter, rightShutter]);
        door.addEventListener("transitionend", (event) => {
            if (event.propertyName === "transform" && shutters.delete(event.target) && shutters.size === 0) {
                door.hidden = true;
            }
        });

        const available = Boolean(day.dataset.movieTitle?.trim());
        if (available && openedDays.has(date.dateTime)) {
            openDoor(true);
        }

        return { day, date, door, doorLabel, available };
    });

    doors.forEach(({ date, door, doorLabel, available }) => {
        door.disabled = !available;
        doorLabel.textContent = available ? text.open : text.locked;
        door.setAttribute("aria-label", `${available ? text.open : text.locked}: ${date.textContent}`);
    });
})();
