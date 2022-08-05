<?php
    //include "core.inc.php";
	include "../database_connection.php";
	
	$search_letters = $_POST['search_letters'];
	
	
	$product_barcode = $conn->query("SELECT * FROM `products` WHERE `barcode` = '$search_letters' `id` DESC  LIMIT 1 ");
	
	
	if(  $bar_row = $product_barcode->fetch_array()  ){
		
		//Checking the Number of Rows Returned
		$query_barcodes_rows = $bar_row->num_rows;
		
		
		if($query_barcodes_rows == 1 ){
			
			
			echo "Barcode found";
			
			
			}else{
			
			
			
			
			
			
			$product_details = $conn->query("SELECT * FROM `products` WHERE `product_name` LIKE '%$search_letters%' OR `barcode` LIKE '%$search_letters%' ORDER BY `id` DESC  LIMIT 5 ");
			echo '<table>';
			while($details_row = $product_details->fetch_array()){
				
				//Device post_office_address
				$product_id = $details_row['id'];
				$barcode = $details_row['barcode'];
				$product_name = $details_row['product_name'];
				$product_description = $details_row['product_description'];
				$unit_price = $details_row['unit_price'];
				$selling_price = $details_row['selling_price'];
				$quantity = $details_row['quantity'];
				
				//NUMBER FORMARTS
				$unit_price = number_format($unit_price);
				$selling_price = number_format($selling_price);
				
				//BACKGROUND COLORS
				$in_stock = '';
				$less_than_5 = '#721818';
				$less_than_10 = 'Gold';
				
				
				if( $quantity >= 10 ){
					$bg_color = $in_stock;
					}else if( $quantity <= 10 && $quantity >= 5 ){
					$bg_color = $less_than_10;
					}else if( $quantity <= 5 ){
					$bg_color = $less_than_5;
				}
				
				echo "
				
				<tr class='row'>
				<td>
				<button type='button' class='btn btn-default btn-md col-md-12' style='text-align: -webkit-auto;'>
				<span style='color: red;'>$barcode </span> | 
				<strong>$product_name $product_description </strong> - 
				$selling_price/=</button><br/>
				</td>
				</tr>
				
				";
				
			}
			echo '</table>';
			
			
			
			
			
			
		}
		
		
		
		
	}
	
	
?>