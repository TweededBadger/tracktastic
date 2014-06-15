angular.module('trackApp')
    .constant("baseUrl", 'data/')
    .controller("ProcessCategoryCtrl",function($scope, $http,baseUrl) {
        $http.get(baseUrl+'process_categories').success(function(data){
            $scope.process_cats = data;
        })
        $scope.$watchCollection('process_cats',function(oldValue,newValue){
            console.log(newValue);
        });
    });