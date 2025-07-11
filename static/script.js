document.addEventListener('DOMContentLoaded', function () {
    let seconds = 5;
    const countdownEl = document.getElementById('countdown');
    if (!countdownEl) {
        return;
    }

    const timer = setInterval(() => {
        seconds--;
        countdownEl.textContent = seconds;
        if (seconds <= 0) {
            clearInterval(timer);
            window.location.href = "/";
        }
    }, 1000);
});

document.addEventListener("DOMContentLoaded", function () {
    const btn = document.getElementById("hamburger");
    const links = document.getElementById("nav-links");
    btn.addEventListener("click", () => {
        links.classList.toggle("open");
    });
});