var myApp = angular.module('myApp', []);

myApp.controller('OutletController', ['$scope', '$http', function($scope, $http) {

    $scope.header = 'Outlets';
  
    var outlet1 = {id:"1", name:"Spotlights"};
    var outlet2 = {id:"2", name:"Stereo"};
    var outlet3 = {id:"3", name:"Table lamp"};
    var outlet4 = {id:"4", name:"Floor lamp"};
    $scope.outlets = {outlet1,outlet2,outlet3,outlet4};
  
    $scope.pressButton = function(id,action) {
        $http.put("/Outlets/api/outlet/"+id, { state : action}).then(function(response) {
        }, function(error) {}
        );
    }
  
}]);