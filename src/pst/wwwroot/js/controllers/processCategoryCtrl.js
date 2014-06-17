angular.module('trackApp')
    .constant("baseUrl", 'data/')
    .controller("ProcessCategoryCtrl",function($scope, $http,baseUrl) {
        $http.get(baseUrl+'process_categories').success(function(data){
            $scope.process_cats = data;
        })
        $scope.$watchCollection('process_cats',function(oldValue,newValue){
            console.log(newValue);
            submitNewOrder(newValue);
        });

        submitNewOrder = function() {

            angular.forEach($scope.process_cats,function(value,key){
               console.log(value);
               console.log(key);
               value.order = key;
            });
            console.log($scope.process_cats);
            $http({
                method:'POST',
                url:baseUrl+'reorder_categories',
                params: {
                    data:$scope.process_cats
                }
            }).success(function(data){
                console.log("------------1")
                console.log(data);

            })
        }

    });