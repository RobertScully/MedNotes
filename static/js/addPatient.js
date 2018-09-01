$(function(){
	$('#btnAddPatient').click(function(){

		var employeedata= '&'
		
		employeedata = employeedata + $("#inputEmployees").serialize();

		$('#inputEmployeeString').val(employeedata);

		$.ajax({
			url: '/addPatient',
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
