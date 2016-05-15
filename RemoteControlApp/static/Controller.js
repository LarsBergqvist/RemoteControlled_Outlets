var myApp = angular.module('myApp', []);

myApp.controller('OutletController', ['$scope', '$http', function($scope, $http) {

    $scope.header = 'Outlets';
  
    var getOutletInfo = function() {
        $http.get("api/outlets").then(function(response) {
            var outlets = response.data.outlets;
            $scope.outlets = outlets;
        }, function(error) {}
        );
    };
  
    $scope.pressButton = function(id,action) {
        $http.put("api/outlets/"+id, { state : action}).then(function(response) {
        }, function(error) {}
        );
    }

    getOutletInfo();
  
}]);