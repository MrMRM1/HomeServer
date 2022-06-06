$(document).ready(function(){
$('.image-popup-vertical-fit').magnificPopup({
	type: 'image',
  mainClass: 'mfp-with-zoom', 
  gallery:{
			enabled:true
		},

  zoom: {
    enabled: true, 

    duration: 300, // duration of the effect, in milliseconds
    easing: 'ease-in-out', // CSS transition easing function

    opener: function(openerElement) {
	
      return openerElement.is('img') ? openerElement : openerElement.find('img');
  }
}

});

});
    $(function() {
      $(".img-fluid").slice(0, 6).show();
      $("#load").click(function(e) {
        e.preventDefault();
        $(".img-fluid:hidden").slice(0, 6).show();
        if ($(".img-fluid:hidden").length == 0) {
          alert("No more image");
        }
      });
    });