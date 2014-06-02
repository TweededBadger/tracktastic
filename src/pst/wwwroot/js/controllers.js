var tracktastic = angular.module('tracktastic', []);

tracktastic.controller('TracktasticCtrl',
    ['$scope','$http',
    function ($scope,$http) {
    $http.get("data/processes/").success(function(data){
       $scope.processes = data;
    });

//  $scope.processes = [
//    {'title': 'Nexus S',
//     'snippet': 'Fast just got faster with Nexus S.','age':1},
//    {'title': 'Motorola XOOM with Wi-Fi',
//     'snippet': 'The Next, Next Generation tablet.','age':2},
//    {'title': 'MOTOROLA XOOM',
//     'snippet': 'The Next, Next Generation tablet.','age':3}
//  ];

//    $scope.name = "World";
    $scope.orderProp = 'age';
}]);