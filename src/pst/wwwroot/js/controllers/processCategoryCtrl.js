angular.module('trackApp')
    .constant("baseUrl", 'data/')
    .controller("ProcessCategoryCtrl",function($scope, $http,baseUrl) {

        $scope.$watchCollection('process_cats',function(oldValue,newValue){
            console.log(newValue);
            submitNewOrder(newValue);
        });

        refreshData = function() {
            $http.get(baseUrl+'process_categories').success(function(data){
                $scope.process_cats = data;
            })
        }

        $scope.addNewCategory = function(newCat) {
            console.log(newCat);
            $http({
                method:'POST',
                url:baseUrl+'/process_categories',
                params: {
                    title:newCat.title,
                    title_search:newCat.title_search,
                    filename_search:newCat.filename_search,
                    assign:1
                }
            }).success(function(data){
                console.log(data);
                $scope.process_cats = data;
            })
        }
        $scope.deleteCat = function(cat) {
            console.log(cat);
            $http({
                method:'DELETE',
                url:baseUrl+'/process_categories',
                params: {
                    id:cat.id
                }
            }).success(function(data){
                console.log(data);
                $scope.process_cats = data;
            })
        }
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
                    data:$scope.process_cats,
                    assign:1
                }
            }).success(function(data){
                console.log("------------1")
                console.log(data);

            })
        }

        refreshData();

    });