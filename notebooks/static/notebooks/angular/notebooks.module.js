// load module and config that Angular tags are put between "{$ $}"
var notebooks = angular.module("notebooks", [])
	.config(function($interpolateProvider) {
	    $interpolateProvider.startSymbol("{$");
	    $interpolateProvider.endSymbol("$}");
	});

