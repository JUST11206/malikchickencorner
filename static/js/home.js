// ======================================
// Hero Button Animation
// ======================================

const heroBtn = document.querySelector(".hero .btn");

if (heroBtn) {

    heroBtn.addEventListener("mouseenter", () => {

        heroBtn.style.transform = "scale(1.08)";

    });

    heroBtn.addEventListener("mouseleave", () => {

        heroBtn.style.transform = "scale(1)";

    });

}

// ======================================
// Fade Animation on Scroll
// ======================================

const observer = new IntersectionObserver((entries) => {

    entries.forEach((entry) => {

        if (entry.isIntersecting) {

            entry.target.classList.add("show");

        }

    });

});

document.querySelectorAll(".animate").forEach((el) => {

    observer.observe(el);

});