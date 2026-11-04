(function () {
    const banner = document.getElementById("christmas-event-banner");
    if (!banner) return;

    const translations = {
        it: {
            countdownTitle: "Tieni pronto per l’evento di Natale!",
            eventTitle: "L’evento di Natale è in corso! Apri l’app ogni giorno.",
            wishesTitle: "Buon Natale da Episora-WatchMate!",
            days: "g", hours: "h", minutes: "min", seconds: "s",
            countdownLink: "Scopri l’evento",
            eventLink: "Vai alla pagina dell’evento",
            wishesLink: "Rivivi l’evento di Natale"
        },
        en: {
            countdownTitle: "Get ready for the Christmas event!",
            eventTitle: "The Christmas event is on! Open the app every day.",
            wishesTitle: "Merry Christmas from Episora-WatchMate!",
            days: "d", hours: "h", minutes: "m", seconds: "s",
            countdownLink: "Discover the event",
            eventLink: "Visit the event page",
            wishesLink: "Visit the Christmas event page"
        },
        es: {
            countdownTitle: "¡Prepárate para el evento de Navidad!",
            eventTitle: "¡El evento de Navidad está en marcha! Abre la app cada día.",
            wishesTitle: "¡Episora-WatchMate te desea una feliz Navidad!",
            days: "d", hours: "h", minutes: "min", seconds: "s",
            countdownLink: "Descubre el evento",
            eventLink: "Visita la página del evento",
            wishesLink: "Visita el evento de Navidad"
        },
        fr: {
            countdownTitle: "Préparez-vous pour l’événement de Noël !",
            eventTitle: "L’événement de Noël est en cours ! Ouvrez l’application chaque jour.",
            wishesTitle: "Joyeux Noël de la part d’Episora-WatchMate !",
            days: "j", hours: "h", minutes: "min", seconds: "s",
            countdownLink: "Découvrez l’événement",
            eventLink: "Voir la page de l’événement",
            wishesLink: "Retrouvez l’événement de Noël"
        },
        de: {
            countdownTitle: "Mach dich bereit für das Weihnachtsevent!",
            eventTitle: "Das Weihnachtsevent läuft! Öffne die App jeden Tag.",
            wishesTitle: "Frohe Weihnachten wünscht Episora-WatchMate!",
            days: "T", hours: "Std.", minutes: "Min.", seconds: "Sek.",
            countdownLink: "Event entdecken",
            eventLink: "Event-Seite öffnen",
            wishesLink: "Weihnachtsevent ansehen"
        },
        ru: {
            countdownTitle: "Приготовьтесь к рождественскому событию!",
            eventTitle: "Рождественское событие уже идёт! Открывайте приложение каждый день.",
            wishesTitle: "Episora-WatchMate поздравляет с Рождеством!",
            days: "дн.", hours: "ч", minutes: "мин.", seconds: "с",
            countdownLink: "Узнать о событии",
            eventLink: "Открыть страницу события",
            wishesLink: "Перейти к рождественскому событию"
        }
    };

    const eventPages = {
        it: "film-natale-2026-italiano.html",
        en: "christmas-movies-2026.html",
        es: "peliculas-navidad-2026.html",
        fr: "films-noel-2026.html",
        de: "weihnachtsfilme-2026.html",
        ru: "rozhdestvenskie-filmy-2026.html"
    };

    const lang = document.documentElement.lang.slice(0, 2).toLowerCase();
    const text = translations[lang];
    const page = eventPages[lang];
    if (!text || !page) {
        throw new Error("Missing Christmas event banner translation or page for " + lang);
    }

    const mascot = document.createElement("img");
    mascot.className = "christmas-event-banner__mascot";
    mascot.src = "Sora_nella_slitta_natalizia_scintillante.png";
    mascot.alt = "";
    mascot.width = 112;
    mascot.height = 112;

    const content = document.createElement("span");
    content.className = "christmas-event-banner__content";

    const title = document.createElement("span");
    title.className = "christmas-event-banner__title";
    title.id = "christmas-event-title";

    const details = document.createElement("span");
    details.className = "christmas-event-banner__countdown";
    details.id = "christmas-event-countdown";

    const linkLabel = document.createElement("span");
    linkLabel.className = "christmas-event-banner__link";

    content.append(title, details, linkLabel);
    banner.append(mascot, content);
    banner.href = page;
    banner.setAttribute("aria-labelledby", title.id);
    banner.setAttribute("aria-describedby", details.id);

    function render() {
        const now = new Date();
        const startOfToday = new Date(now.getFullYear(), now.getMonth(), now.getDate());
        const preEventStart = new Date(2026, 10, 1);
        const eventStart = new Date(2026, 11, 1);
        const eventEnd = new Date(2026, 11, 25);
        const wishesEnd = new Date(2026, 11, 26);

        if (startOfToday < preEventStart || startOfToday >= wishesEnd) {
            banner.hidden = true;
            return;
        }

        banner.hidden = false;
        if (startOfToday < eventStart) {
            const remaining = Math.max(0, eventStart.getTime() - now.getTime());
            const seconds = Math.floor(remaining / 1000);
            const days = Math.floor(seconds / 86400);
            const hours = Math.floor((seconds % 86400) / 3600);
            const minutes = Math.floor((seconds % 3600) / 60);
            const secs = seconds % 60;

            title.textContent = text.countdownTitle;
            details.textContent = `${days}${text.days} ${hours}${text.hours} ${minutes}${text.minutes} ${secs}${text.seconds}`;
            linkLabel.textContent = text.countdownLink;
            banner.dataset.phase = "countdown";
        } else if (startOfToday < eventEnd) {
            title.textContent = text.eventTitle;
            details.textContent = "";
            linkLabel.textContent = text.eventLink;
            banner.dataset.phase = "active";
        } else {
            title.textContent = text.wishesTitle;
            details.textContent = "";
            linkLabel.textContent = text.wishesLink;
            banner.dataset.phase = "wishes";
        }
    }

    render();
    window.setInterval(render, 1000);
})();
