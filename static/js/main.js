// ================================
// Navbar Scroll Effect
// ================================

window.addEventListener("scroll", function () {

    const navbar = document.querySelector(".custom-navbar");

    if (window.scrollY > 50) {

        navbar.classList.add("scrolled");

    } else {

        navbar.classList.remove("scrolled");

    }

});

// ================================
// Smooth Scroll
// ================================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {

    anchor.addEventListener("click", function (e) {

        e.preventDefault();

        document.querySelector(this.getAttribute("href"))
            ?.scrollIntoView({

                behavior: "smooth"

            });

    });

});

// ================================
// Current Year
// ================================

const year = document.getElementById("year");

if (year) {

    year.textContent = new Date().getFullYear();

}