/*

	$('#search_item_field').focusout(function(){
		
*/
$(document).ready(function() {
	
	
	
	
	$('#search_item_field').keyup(function(){
		
		var search_letters = $(this).val();
		
		//$('#product_search_results').html("kamoga");
		
		var url = "customization/search_products.php";
		
		$.post(url, {search_letters: search_letters},function(data){
			$("#product_search_results").html(data).show();
		});
		
		//alert("key up -" + letter );
		
		
		
		
	});
	
	
	
	
	
	
	
	
});