

// $(document).ready(function() {
//     const modal = $('.modal');
//     let slideIndex = 1;

//     // Open modal on .showModal button click
//     $('.showModal').click(function(event) {
//         modal.addClass('is-active');
//         showSlides(); // Start slideshow when modal is opened
//     });

//     // Close modal on .closeModal button click
//     $('.modal-close').click(function(event) {
//         modal.removeClass('is-active');
//         clearTimeout(slideTimeout); // Stop slideshow when modal is closed
//     });

//     // Close modal when background is clicked
//     $('.modal-background').click(function(event) {
//         modal.removeClass('is-active');
//         clearTimeout(slideTimeout); // Stop slideshow when modal is closed
//     });

//     // Function to handle slideshow
//     let slideTimeout; // Declare variable for timeout reference
//     function showSlides() {
//         let i;
//         let slides = document.getElementsByClassName("mySlides");

//         for (i = 0; i < slides.length; i++) {
//             slides[i].style.display = "none"; // Hide all slides
//         }

//         slideIndex++;
//         if (slideIndex > slides.length) { slideIndex = 1 } // Reset to first slide if out of bounds
//         slides[slideIndex - 1].style.display = "block"; // Show the current slide

//         slideTimeout = setTimeout(showSlides, 2000); // Change slide every 2 seconds
//     }
// });





$(document).ready(function() {
    const modal = $('.modal');
    let slideIndex = 0; // Start at the first slide
    let slideTimeout; // Variable to hold the timeout ID for slideshow

    // Open modal on .showModal button click
    $('.showModal').click(function(event) {
        modal.addClass('is-active');
        showSlides(); // Start slideshow when modal is opened
    });

    // Close modal on .modal-close button click
    $('.modal-close').click(function(event) {
        closeModal(); // Close modal and stop slideshow
    });

    // Close modal when background is clicked
    $('.modal-background').click(function(event) {
        closeModal(); // Close modal and stop slideshow
    });

    // Function to stop the slideshow and close the modal
    function closeModal() {
        modal.removeClass('is-active');
        clearTimeout(slideTimeout); // Stop the slideshow when modal is closed
    }

    // Function to handle slideshow
    function showSlides() {
        let slides = $(".mySlides-fade"); // Use the correct class for the slides

        // Hide all slides initially
        slides.each(function() {
            $(this).css('display', 'none');
        });

        // Increment the slide index
        slideIndex++;

        // If we've gone past the last slide, reset to the first
        if (slideIndex > slides.length) {
            slideIndex = 1;
        }

        // Show the current slide
        $(slides[slideIndex - 1]).css('display', 'block');

        // Change slide every 3 seconds (adjust timing as needed)
        slideTimeout = setTimeout(showSlides, 3000);
    }
});





