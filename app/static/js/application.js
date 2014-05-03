(function($) {
	$.fn.ajaxSubmit = function(options) {
		if(!options) options = {};

		var self = $(this);
		var inputChild = self.find('input:not([type="hidden"])'),
			btnChild = self.find('button');
		var required = options.required,
			onSuccess = options.success,
			errorType = options.errorType,
			onError = options.error;

		self.submit(function() {
			if(required) {
				for(var i = 0; i < required.length; i++) {
					var name = required[i];
					var element = $('[name="' + name + '"]');
					var field = element.attr('placeholder');

					if(element.val() == '') {
						alert('Please fill the required field: ' + field);
						element.focus();
						return false;
					}
				}
			}

			$.ajax({
				url: self.attr('action'),
				type: self.attr('method'),
				data: self.serialize(),
				beforeSend: function() {
					inputChild.attr('disabled', 'disabled');
					btnChild.attr('disabled', 'disabled');
				},
				success: function(data) {
					if(data.success) {
						if(data.alertMessage) {
							alert(data.alertMessage);
						}

						if(onSuccess) {
							onSuccess(data);
						}
					} else {
						if(data.errors) {
							if(errorType == 'alert') {
								for(var i = 0; i < data.errors.length; i++) {
									var err = data.errors[i];
									alert(err.field + ': ' + err.error);
								}
							} else if(errorType == 'function' && onError && typeof(onError) == 'function') {
								onError.call(self, data.errors);
							}
						}
					}
				},
				error: function(jqXHR, textStatus, err) {
					alert(err);
				},
				complete: function() {
					inputChild.val('').removeAttr('disabled');
					btnChild.removeAttr('disabled');
				}
			});

			return false;
		});
	};
})(jQuery);