angular.module('trackApp')
    .controller("PickerCtrl", function ($scope) {
        $scope.today = function () {
            $scope.dt = new Date();
        };
        $scope.today();
        $scope.open = function ($event) {
            $event.preventDefault();
            $event.stopPropagation();
            $scope.opened = true;
        }
        $scope.dateOptions = {
            formatYear: 'yy',
            startingDay: 1
        };
        $scope.$watch('dt',function(oldValue,newValue){
            console.log("Date Picked 2: "+newValue);
        });

    });