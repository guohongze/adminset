# jGrowl 
jGrowl is a jQuery plugin that raises unobtrusive messages within the browser, similar to the way that OS X's Growl Framework works. The idea is simple, deliver notifications to the end user in a noticeable way that doesn't obstruct the work flow and yet keeps the user informed.

## Example usages
	// Sample 1
	$.jGrowl("Hello world!");
	// Sample 2
	$.jGrowl("Stick this!", { sticky: true });
	// Sample 3
	$.jGrowl("A message with a header", { header: 'Important' });
	// Sample 4
	$.jGrowl("A message that will live a little longer.", { life: 10000 });
	// Sample 5
	$.jGrowl("A message with a beforeOpen callback and a different opening animation.", {
		beforeClose: function(e,m) {
			alert('About to close this notification!');
		},
		animateOpen: {
			height: 'show'
		}
	});

