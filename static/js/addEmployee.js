$(function(){
	$('#btnAddEmployee').click(function(){
			
		$.ajax({
			url: '/addEmployee',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});

