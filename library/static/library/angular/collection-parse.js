library.controller("collectionCtrl", function($scope, $http) {
	// Loader service for database JSON.
	// Deferred forces function to first get the json file
	// from the server and then return it.

	var collections = $http.get("/api/?model=librarycollection")
		.then(function(data) {
			$scope.collections = data.data.items;
		});

	$scope.fetch = function(id) {
		// find a collection based on id and return its title
		$scope.fetched = $scope.collections.filter(function(entry) {
				return entry.id === id;
			})[0];
		}
});

library.filter('markdown', function ($sce) {
    var converter = new Showdown.converter();
    return function (value) {
		var html = converter.makeHtml(value || '');
		if (html.length > 1) {
        	return $sce.trustAsHtml(html.slice(0, 700) + '...');
		} else {
			return $sce.trustAsHtml('<p class="small">No content found.</p>');
		}
    };
});
