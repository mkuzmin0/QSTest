var json = '[{"text": "Parent 1"}]';
$('#cash_tree').treeview({
	data: json,
	onNodeSelected: function(event, node) {
	  $('#selected_node_value').val(node.text);
	  $('#selected_node_id').val(node.id);
	},
	
});
//$('#db_tree').treeview({data: json});

var get_selected_node_id = function(){
	return $('#selected_node_id').val();
};

var get_selected_node_value = function(){
	return $('#selected_node_value').val();
};
var load_cache_tree = function(){
	$.ajax({
		url: '/cache_tree',
		type: 'GET',
		success: function (result) {
		  $('#cash_tree').treeview({data: json});
		},
		error: function(result){
			alert('Error was during the loading cache tree.');
		}
	});  
};
var load_db_tree = function(){
	$.ajax({
		url: '/db_tree',
		type: 'GET',
		success: function (result) {
		    //alert(result);
		  $('#db_tree').treeview({data: result});
		},
		error: function(result){
			alert('Error was during the loading db tree.');
		}
	});  
};
load_db_tree();

$('#add_button').click(function() { 
	$.ajax({
		url: '/add',
		type: 'POST',
		data: {
			'id': get_selected_node_id(),
			'value': get_selected_node_value()
		},
		success: function (result) {
		  load_cache_tree();
		},
		error: function(result){
			alert('Error was during adding new node.');
		}
	});  
});

$('#edit_button').click(function() { 
	var node_id = get_selected_node_id();
	var node_value = get_selected_node_value();
	
	if (node_id) {
		$.ajax({
			url: '/edit',
			type: 'POST',
			data: {
				'id': node_id,
				'value': node_value
			},
			success: function (result) {
			  load_cache_tree();
			},
			error: function(result){
				alert('Error was during editing node.');
			}
		});  
	} else {
		alert('Node is not selected.');
	}
});

$('#delete_button').click(function() { 
	var node_id = get_selected_node_id();
	if (node_id) {
		$.ajax({
			url: '/delete',
			type: 'POST',
			data: {
				'id': node_id
			},
			success: function (result) {
			  load_cache_tree();
			},
			error: function(result){
				alert('Error was during node delete.');
			}
		});  
	} else {
		alert('Node is not selected.');
	}
});

$('#save_button').click(function() { 
	$.ajax({
		url: '/save',
		type: 'POST',
		success: function (result) {
		  load_cache_tree();
		  load_db_tree();
		},
		error: function(result){
			alert('Error was during saving.');
		}
	});  
});

$('#reset_button').click(function() { 
	$.ajax({
		url: '/reset',
		type: 'POST',
		success: function (result) {
		  load_cache_tree();
		  load_db_tree();
		},
		error: function(result){
			alert('Error was during db reset.');
		}
	});  
});
