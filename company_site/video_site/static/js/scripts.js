/*!
* Start Bootstrap - Full Width Pics v5.0.6 (https://startbootstrap.com/template/full-width-pics)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-full-width-pics/blob/master/LICENSE)
*/
<script>
    function scrollMovies(direction) {
    const movieRow = document.querySelector('.movie-row');
    const scrollAmount = 300; // Adjust this value to how far the row should scroll per click
    const rowWidth = movieRow.scrollWidth;
    const containerWidth = movieRow.parentElement.offsetWidth;

    if (direction === 1) {
        // Scroll to the right
        movieRow.scrollBy({
            left: scrollAmount,
            behavior: 'smooth'
        });

        // Loop to the first movie when reaching the end
        if (movieRow.scrollLeft >= rowWidth - containerWidth) {
            movieRow.scrollLeft = 0;
        }
    } else {
        // Scroll to the left
        movieRow.scrollBy({
            left: -scrollAmount,
            behavior: 'smooth'
        });

        // Loop to the last movie when reaching the start
        if (movieRow.scrollLeft <= 0) {
            movieRow.scrollLeft = rowWidth - containerWidth;
        }
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const leftButton = document.querySelector('.scroll-btn.left');
    const rightButton = document.querySelector('.scroll-btn.right');

    // You already have the buttons in the HTML with onclick handlers
    // No need to add event listeners here as they're already handled by the inline onclick
});
</script>
