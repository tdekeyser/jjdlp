// load module and config that Angular tags are put between "{$ $}"
var library = angular.module("library", [])
	.config(function($interpolateProvider) {
	    $interpolateProvider.startSymbol("{$");
	    $interpolateProvider.endSymbol("$}");
	});

