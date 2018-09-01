$(function(){
	$('#btnAddNote').click(function(){
		$.ajax({
			url: '/insertNote',
			data: $('#noteForm').serialize(),
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