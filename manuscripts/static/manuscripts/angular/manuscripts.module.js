// load module and config that Angular tags are put between "{$ $}"
var manuscripts = angular.module("manuscripts", [])
	.config(function($interpolateProvider) {
	    $interpolateProvider.startSymbol("{$");
	    $interpolateProvider.endSymbol("$}");
	});

