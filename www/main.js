$(document).ready(function () {
    // Initialize Textillate
    $(".text").textillate({
        loop: true,
        sync: true,
        in: { effect: "fadeIn", sync: false, delay: 100 },
        out: { effect: "fadeOutUp", sync: true }
    });

});
