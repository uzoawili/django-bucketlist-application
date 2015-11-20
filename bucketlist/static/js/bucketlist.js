

$(document).ready(function() {

  //----------------------------------------
  //  Staggered list effect:
  //----------------------------------------

  //show the hero items using staggered list effect:
  Materialize.showStaggeredList('#hero-items');
  Materialize.showStaggeredList('.user-options');
  // Materialize.showStaggeredList('.thumb-list');


    //----------------------------------------


  //----------------------------------------
  //  Packery grids:
  //----------------------------------------
    
  // initialize Packery on the grids:
  var $grid = $('.packery-grid');

  $grid.packery({

      'itemSelector': '.grid-item',
      'columnWidth': '.grid-sizer',
      'gutter': '.gutter-sizer',
      'percentPosition': true,
      'isResizeBound': true

  });


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

  //get the index of the active auth panel:
  active_auth_index = $('.auth-panels').data('activeAuthIndex')

  //initialize Flickity on the auth panels:
  $authPanels = $('.auth-panels').flickity({
  
    cellSelector: '.panel',
    setGallerySize: true,
    draggable: false,
    freeScroll: false,
    prevNextButtons: false,
    pageDots: false,
    initialIndex: active_auth_index

  });

  $('#signin-link').click(function(){
    $authPanels.flickity( 'select', 1 );
  })

  $('#signup-link').click(function(){
    $authPanels.flickity( 'select', 0 );
  })



  //----------------------------------------
  //  Sidebar:
  //----------------------------------------

  //initialize the Materialize Sidenav:
  $('.button-collapse').sideNav();
  


  //----------------------------------------
  //  Modals:
  //----------------------------------------

  //set listeners for modal triggers' click:
  $('.thumb-list').on('click', 'a.modal-trigger', function(e) {
    e.preventDefault();

    $target = $($(this).data('target'));
    $targetForm = $target.find('form');
    targetAction = $(this).attr('href');

    if(targetAction && $targetForm){
      $targetForm.attr('action', targetAction);
    }

    $target.openModal({
      dismissible: true,
      opacity: .85,
    }); 
  });


});