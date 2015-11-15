

$(document).ready(function() {

  //----------------------------------------
  //  Staggered list effect:
  //----------------------------------------

  //show the hero items using staggered list effect:
  Materialize.showStaggeredList('#hero-items');
  Materialize.showStaggeredList('.user-options');
  Materialize.showStaggeredList('.thumb-list');


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

  // initialize MaterializeCSS lean modals on the triggers
  $('.modal-trigger').leanModal({
    dismissible: true,
    opacity: .95,
  });

  // set listeners for modal trigger click and submit:

  $('.modal-trigger').on('click', function(){
    targetForm = $("#" + $(this).data('target') + " form");
    targetAction = $(this).data('targetAction');
    targetMethod = $(this).data('targetMethod');
    if(targetForm){
      if(targetAction) targetForm.attr('action', targetAction);
      if(targetMethod) targetForm.attr('method', targetMethod);
    }
  });

  $('.modal form').on('submit', function(event){
    event.preventDefault();
    submitForm(this);
  });

  // map the form operations to response handler functions:
  formResponseHandlers = {
    'create_bucket_list': onCreateBucketList
    // 'update_bucket_list':,
    // 'delete_bucket_list':,
    // 'create_bucket_list_item':,
    // 'update_bucket_list_item':,
    // 'delete_bucket_list_item':
  };

  function submitForm(form) {
    $.ajax({
      url : form.action,
      type : form.method,
      data : $(form).serialize(),
      dataType: 'json',
      headers: {
        'X-CSRFToken': $(form).find('input[name="csrfmiddlewaretoken"]').val()
      },
      success : function(json_response) {
        try{ 
          //call the appropriate response handler function:
          responseHandler = formResponseHandlers[json_response.operation];
          responseHandler(json_response);
        } catch(e){
          // show error message:
          onFormSubmitError(form);
        }
      },
      error : function() {
        // show error message:
        onFormSubmitError(form);
      }
    });
  };

  function onFormSubmitError(form) {
    messages = $(form).find('.messages');
    messages.text('Sorry, something went wrong. Your request could not be completed.');
  }

  function onCreateBucketList(response){
    $modal = $('#new-bucketlist-modal')
    if (response.status == 'success'){
      // crreate the thumblist if it doesn't exist:
      if (! $('.thumb-list-container .thumb-list').length){
        $('.thumb-list-container').empty().append('<ul class="thumb-list"></ul>');
      }
      // add new item to the thumbs-list:
      $('.thumb-list').prepend(response.html);
      // close the modal:
      $modal.closeModal();
      //show toast:
      Materialize.toast('Bucket list added. Noice!', 4000);

    } else if (response.status == 'invalid'){
      // replace the content of the modal with the response data:
      $modal.html(response.html);
      // show the modal again if it happened to closed:
      $modal.showModal();
    }
  }



});