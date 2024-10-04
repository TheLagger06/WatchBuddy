// script.js
document.addEventListener('DOMContentLoaded', function () {
    const slideshows = document.querySelectorAll('.slideshow');

    slideshows.forEach(slideshow => {
        const images = slideshow.querySelectorAll('img');
        let currentIndex = 0;

        // Automatically show the first image
        images[currentIndex].style.display = 'block';

        // Change images every 3 seconds
        setInterval(() => {
            images[currentIndex].style.display = 'none'; // Hide current image
            currentIndex = (currentIndex + 1) % images.length; // Move to the next image
            images[currentIndex].style.display = 'block'; // Show next image
        }, 3000);
    });
});

document.getElementById('search-icon').addEventListener('click', function() {
    const searchInput = document.getElementById('search-input');
    searchInput.style.display = searchInput.style.display === 'none' ? 'block' : 'none';
});

  function toggleEpisodes(seasonId) {
        const episodesContainer = document.getElementById(`episodes-${seasonId}`);
        if (episodesContainer.style.display === "none") {
            episodesContainer.style.display = "block";
        } else {
            episodesContainer.style.display = "none";
        }
}


    document.addEventListener('DOMContentLoaded', function () {
        // When "Register" is clicked, hide login modal and show register modal
        document.getElementById('openRegisterModal').addEventListener('click', function () {
            $('#loginModal').modal('hide');
            setTimeout(function () {
                $('#registerModal').modal('show');
            }, 500);
        });

        // When "Login here" is clicked, hide register modal and show login modal
        document.getElementById('openLoginModal').addEventListener('click', function () {
            $('#registerModal').modal('hide');
            setTimeout(function () {
                $('#loginModal').modal('show');
            }, 500);
        });
    });
