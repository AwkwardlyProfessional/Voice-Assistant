$(document).ready(function () {
    // Expose the function for Python to call
    eel.expose(DisplayMessage);

    // Define the function that displays the message in the frontend
    function DisplayMessage(message) {
        // Update the UI with the message (corrected the class selector)
        $(".siri-message:first").text(message); 
        $('.siri-message').textillate('start');  // Start text animation
    }
    // Display hood
    eel.expose(ShowHood)
    function ShowHood() {
        $("#Oval").attr("hidden", false);
        $("#SiriWave").attr("hidden", true);
    }
});
