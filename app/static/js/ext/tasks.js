$('a.task-name').editable({
	type: 'text',
	url: URL_TASKS,
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
$('a.task-storage').editable({
	type: 'select',
	url: URL_TASKS,
	source: URL_STORAGES,
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
$('a.task-time').editable({
	type: 'select',
	url: URL_TASKS,
	source: (function() {
		var source = [];
		for(var i = 0; i < 48; i++) {
			source.push({
				'value': i,
				'text': '{0}:{1}'.format(parseInt(i / 2).zeroPad(10), (i % 2 == 1 ? 30 : 0).zeroPad(10)),
			});
		}

		return source;
	})(),
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
$('a.del-task').editable({
	type: 'password',
	url: URL_TASKS,
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
$('#add-task-form').ajaxSubmit({
	required: FORM_ELEMENTS,
	errorType: 'function',
	error: function(errors) {
		var messages = $(this).find('div.messages');
		messages.html('');
		for(var i = 0; i < errors.length; i++) {
			var err = errors[i];
			messages.append('<div class="alert alert-danger"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button> ' + err.field + ': ' + err.error + '</div>');
		}
	},
	success: function() {
		location.reload();
	}
});
