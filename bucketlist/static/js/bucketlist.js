

$(document).ready(function() {

    //----------------------------------------
    //  Background Slideshow:
    //----------------------------------------

    //initialize slider on the background images:
    $slider = $('.bg-img .slider').slider({

        full_width: true,
        indicators: false,
        transition: 2000,
        interval: 10000

    });

    //----------------------------------------
    //  Auth Panels:
    //----------------------------------------

    //initialize Flickity on the auth panels:
    $authPanels = $('.auth-panels').flickity({
    
        cellSelector: '.panel',
        setGallerySize: true,
        freeScroll: false,
        prevNextButtons: false,
        pageDots: false

    });

    $('#signin-link').click(function(){
        $authPanels.flickity( 'select', 1 );
    })

    $('#signup-link').click(function(){
        $authPanels.flickity( 'select', 0 );
    })

    //----------------------------------------
    //  Hero:
    //----------------------------------------

    //show the hero items using staggered list effect:
    Materialize.showStaggeredList('#hero-items');

});