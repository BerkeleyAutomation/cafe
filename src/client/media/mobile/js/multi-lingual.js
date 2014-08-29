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
				$('.instructions').html('Click any mug to begin.');
				$('.instructions2').html('We want to hear your idea. Please rate one more suggestion first.');
				$('.instructions3').html('Click your mug (in green) to share your suggestion.');
                $("#zipcode-error").html('Zipcode must be 5 digits');
				window.spanish = 'english';				
			} else {
				$('.english').hide();
				$('.spanish').show();
				$('.instructions').html('Haga clic en cualquier taza para comenzar.');
				$('.instructions2').html('Queremos escuchar tu idea pero primero, por favor, califique una sugerencia más.');
				$('.instructions3').html('Haga clic en su taza (en verde) para compartir su sugerencia.');
                $("#zipcode-error").html('El código postal debe tener 5 dígitos');

				window.spanish = 'spanish';				
			}	
		}
	);


});