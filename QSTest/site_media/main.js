var get_selected_node_id = function(){
	return $('#selected_node_id').val();
};

var get_selected_db_node_id = function(){
	return $('#selected_db_node_id').val();
};


var get_selected_node_value = function(){
	return $('#selected_node_value').val();
};
var load_cache_tree = function(){
	$.ajax({
		url: '/cache_tree',
		type: 'GET',
		success: function (result) {
			//alert(result);
			$('#cash_tree').treeview({
				data: result,
				onNodeSelected: function(event, node) {
	                $('#selected_node_value').val(node.text);
	                $('#selected_node_id').val(node.id);
	            }
			});
		},
		error: function(result){
			alert('An error occurred during the cache tree load request.');
		}
	});  
};
load_cache_tree();

var load_db_tree = function(){
	$.ajax({
		url: '/db_tree',
		type: 'GET',
		success: function (result) {
		    //alert(result);

			$('#db_tree').treeview({
				data: result,
				onNodeSelected: function(event, node) {
	  				$('#selected_db_node_id').val(node.id);
				},
		  	});
		},
		error: function(result){
			alert('An error occurred during the db tree load request.');
		}
	});  
};
load_db_tree();

$('#add_button').click(function() { 
	$.ajax({
		url: '/add/',
		type: 'POST',
		data: {
			'id': get_selected_node_id(),
			'value': get_selected_node_value()
		},
		success: function (result) {
		    load_cache_tree();
		},
		error: function(result){
			alert('An error occurred during the add node request.');
		}
	});  
});

$('#edit_button').click(function() { 
	var node_id = get_selected_node_id();
	var node_value = get_selected_node_value();
	
	if (node_id) {
		$.ajax({
			url: '/edit/',
			type: 'POST',
			data: {
				'id': node_id,
				'value': node_value
			},
			success: function (result) {
			    load_cache_tree();
			},
			error: function(result){
				alert('An error occurred during the edit node request.');
			}
		});  
	} else {
		alert('Cache node is not selected.');
	}
});

$('#delete_button').click(function() { 
	var node_id = get_selected_node_id();
	if (node_id) {
		$.ajax({
			url: '/delete/',
			type: 'POST',
			data: {
				'id': node_id
			},
			success: function (result) {
			    load_cache_tree();
			    $('#selected_node_value').val('');
	            $('#selected_node_id').val('');
			},
			error: function(result){
				alert('An error occurred during the delete node request.');
			}
		});  
	} else {
		alert('Cache node is not selected.');
	}
});

$('#cache_button').click(function() {
	var node_id = get_selected_db_node_id();
	if (node_id) {
		$.ajax({
			url: '/cache_node/',
			type: 'POST',
			data: {
				'id': node_id
			},
			success: function (result) {
			    //alert(request);
			    load_cache_tree();
			},
			error: function(result){
			    //alert(request);
				alert('An error occurred during the cache node request.');
			}
		});
	} else {
		alert('DB node is not selected.');
	}
});

$('#save_button').click(function() { 
	$.ajax({
		url: '/save/',
		type: 'POST',
		success: function (result) {
		  load_cache_tree();
		  load_db_tree();
		},
		error: function(result){
			alert('An error occurred during the save request.');
		}
	});  
});

$('#reset_button').click(function() { 
	$.ajax({
		url: '/db_reset/',
		type: 'POST',
		success: function (result) {
		    load_cache_tree();
		    load_db_tree();
		    $('#selected_node_value').val('');
	        $('#selected_node_id').val('');
	        $('#selected_db_node_id').val('');
		},
		error: function(result){
			alert('An error occurred during the reset request.');
		}
	});  
});
