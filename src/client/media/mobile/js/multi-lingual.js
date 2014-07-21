 $(document).ready(function()
 {
 	console.log('spanish');
 	console.log(window.spanish);
	if (window.spanish=='spanish') {
		$('.spanish').show();
		$('.english').hide();
	} else {
		$('.english').show();
		$('.spanish').hide();
	}

	$('.landing-translate-btn').click(
		function() 
		{
			if (window.spanish=='spanish') {
				$('.english').show();
				$('.spanish').hide();
				window.spanish = 'english';				
			} else {
				$('.english').hide();
				$('.spanish').show();
				window.spanish = 'spanish';				
			}	
		}
	);


	$('#discuss-home-btn').click
	(
		function ()
		{
        	$('.landing').hide();
        	$('#register').show();
		}
	);
});