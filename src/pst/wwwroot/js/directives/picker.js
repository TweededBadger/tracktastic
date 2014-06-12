angular.module('trackApp')
    .directive('picker', function () {

    return {
        link:function (scope, element, attrs)
        {
            scope.today = function () {
                scope.dt = new Date();
                scope.dt.setHours(0);
                scope.dt.setMinutes(0);
                scope.dt.setSeconds(0);
            };
            scope.today();

            scope.open = function ($event) {
                $event.preventDefault();
                $event.stopPropagation();
                scope.opened = true;
            }
            scope.dateOptions = {
                formatYear: 'yy',
                startingDay: 1
            };
        }
    }
});