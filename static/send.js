$(function() {
	$('#btnSend').click(function() {
 
		$.ajax({
			url: '/query',
			    data: $('form').serialize(),
			    type: 'POST',
			    success: function(response) {
			    console.log(response);
			},
			    error: function(error) {
			    console.log(error);
			}
		    });
	    });
    });