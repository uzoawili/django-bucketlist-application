

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
  $(".button-collapse").sideNav();
  


  //----------------------------------------
  //  Modals:
  //----------------------------------------

  $('.modal-trigger').leanModal({

    dismissible: true,
    opacity: .95,

  });

  $('.modal-trigger').on('click', function(){

  });


  //----------------------------------------
  //  Staggered list effect:
  //----------------------------------------

  //show the hero items using staggered list effect:
  Materialize.showStaggeredList('#hero-items');
  Materialize.showStaggeredList('.user-options');
  Materialize.showStaggeredList('.thumb-list');





  modalForms = $('.modal form');
  modalForms.on('submit', function(event){
    event.preventDefault();
    submitForm(this);
  });

  function submitForm(form) {
    $.ajax({
      url : form.action,
      type : form.method,
      data : $(form).serialize(),
      headers: {
        'X-CSRFToken': $(form).find('input[name="csrfmiddlewaretoken"]').val()
      },
      success : function(data, textStatus, jqXHR) {
        console.log(data);
        console.log(jqXHR.statusCode());
      },
      error : function() {
        messages = $(form).find('.messages');
        messages.text('Sorry, something went wrong. Your request could not be completed.');
      }
    });
  };







});