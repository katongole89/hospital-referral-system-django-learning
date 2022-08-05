
$(document).ready(function(){
	
	//Show the total of the product
	$('#rate').keyup( function(){
		
		var quantity = $('#quantity').val();
		var rate = $('#rate').val();
		
		var product_total = quantity*rate;
		
		$('#product_modal_total').html(product_total);
		
	});
	
	
	//$('#submit_form').submit( function(){
	$('#submit_modal_form_btn').click( function(){
		
		var modal_invoice_number = $('#modal_invoice_number').val();
		var products_name = $('#products_name').val();
		var quantity = $('#quantity').val();
		var rate = $('#rate').val();
		var short_description = $('#short_description').val();
		
		//The TAX
		var tax = $('#tax').val();
		
		
		
		//alert('invo' + modal_invoice_number + products_name + quantity + rate + short_description);
		
		//url
		var url = "add_invoice_product.php";
		
		var url2 = "get_totals.php";
		
		
		$.post(url, {modal_invoice_number: modal_invoice_number, products_name: products_name, quantity: quantity, rate: rate, short_description: short_description},function(data){
			$("#add_product_results").html(data).show(function(){
				
				$.post(url2, {modal_invoice_number: modal_invoice_number, quantity: quantity, rate: rate, tax: tax},function(data){
					$("#invoice_totals").html(data).show();
				});
				
			});
			
			
			
		});
		
	});
	
	
	
	
});
