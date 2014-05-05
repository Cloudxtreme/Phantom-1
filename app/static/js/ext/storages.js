$('a.storage-name').editable({
	type: 'text',
	url: URL_STORAGES,
	ajaxOptions: {
		type: 'PUT',
		dataType: 'json'
	},
	success: function(res, val) {
		if(!res.success) {
			return res.msg;
		}
	}
});
$('a.del-storage').editable({
	type: 'password',
	url: URL_STORAGES,
	value: '',
	title: 'Enter your password',
	ajaxOptions: {
		type: 'DELETE',
		dataType: 'json'
	},
	success: function(res, val) {
		if(!res.success) {
			return res.msg;
		}

		location.reload();
	}
});
$('#add-storage-form').ajaxSubmit({
	required: FORM_ELEMENTS,
	errorType: 'function',
	error: function(errors) {
		var messages = $(this).find('div.messages');
		for(var i = 0; i < errors.length; i++) {
			var err = errors[i];
			messages.append('<div class="alert alert-danger"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button> ' + err.field + ': ' + err.error + '</div>');
		}
	},
	success: function() {
		location.reload();
	}
});