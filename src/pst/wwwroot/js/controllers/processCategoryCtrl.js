angular.module('trackApp')
    .constant("baseUrl", 'data/')
    .controller("ProcessCategoryCtrl",function($scope, $http,baseUrl) {

        $scope.selectedCat = undefined;
        $scope.$watchCollection('process_cats',function(oldValue,newValue){
            submitNewOrder(newValue);
        });

        refreshData = function() {
            $http.get(baseUrl+'process_categories').success(function(data){
                $scope.process_cats = data;
            })
        }

        $scope.addNewCategory = function(newCat) {
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
                $scope.process_cats = data;
            })
        }
        $scope.addNewFilter = function(newFilter){
            if ($scope.selectedCat == undefined) return false;
            $http({
                method:'POST',
                url:baseUrl+'/category_filters',
                params: {
                    category_id:$scope.selectedCat.id,
                    title_search:newFilter.title_search,
                    filename_search:newFilter.filename_search,
                    assign:1
                }
            }).success(function(data){
                $scope.selectedCat.filters = data;
            })
        }
        $scope.deleteFilter = function(filter) {
            if ($scope.selectedCat == undefined) return false;
            $http({
                method:'DELETE',
                url:baseUrl+'/category_filters',
                params: {
                    category_id:$scope.selectedCat.id,
                    id:filter.id,
                    assign:1
                }
            }).success(function(data){
                $scope.selectedCat.filters = data;
            })
        }
        $scope.deleteCat = function(cat) {
            $http({
                method:'DELETE',
                url:baseUrl+'/process_categories',
                params: {
                    id:cat.id,
                    assign:1
                }
            }).success(function(data){
                $scope.process_cats = data;
            })
        }
        $scope.selectCat = function(cat) {
            console.log(cat);
            $scope.selectedCat = cat;
        }
        submitNewOrder = function() {
            if (angular.isUndefined($scope.process_cats)) return false;
            angular.forEach($scope.process_cats,function(value,key){
               value.order = key;
            });
            $http({
                method:'POST',
                url:baseUrl+'reorder_categories',
                params: {
                    data:$scope.process_cats,
                    assign:1
                }
            }).success(function(data){
//                $scope.process_cats = data;
            })
        }

        refreshData();

    });