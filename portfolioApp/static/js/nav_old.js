$(document).ready(function(){  
    $('#nav_logo').click(function(){
        $('#nav-bar').animate({width: 'toggle'});
        $('#nav_logo_hidden').animate({width: 'toggle'});
    });
    $('#nav_logo_hidden').click(function(){
        $('#nav-bar').animate({width: 'toggle'});
        $('#nav_logo_hidden').animate({width: 'toggle'});
    });
    
    /* Set the width of the side navigation to 0 */
    function closeNav() {
        document.getElementById("mySideNav").style.width = "0";
    }

    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
})
});

function openNav() {
    $("#mySideNav").width("60%");
}

/* Set the width of the side navigation to 0 */
function closeNav() {
    document.getElementById("mySideNav").style.width = "0";
}
