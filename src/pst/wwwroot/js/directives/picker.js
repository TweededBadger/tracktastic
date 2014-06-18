angular.module('trackApp')
    .directive('picker', function () {
    return {
        link:function (scope, element, attrs)
        {

            scope.dt = new Date();
            scope.dt.setHours(0);
            scope.dt.setMinutes(0);
            scope.dt.setSeconds(0);
            console.log(scope.dt);

            scope.pickerStartTime = new Date();
            scope.pickerStartTime.setUTCHours(0);
            scope.pickerStartTime.setHours(9)
            scope.pickerStartTime.setMinutes(0)
            scope.pickerStartTime.setSeconds(0);


            scope.pickerEndTime = new Date();
            scope.pickerEndTime.setUTCHours(0);
            scope.pickerEndTime.setHours(23);
            scope.pickerEndTime.setMinutes(59);

            scope.hstep = 1;
            scope.mstep = 1;
            scope.ismeridian = false;

            scope.openStart = function ($event) {
                $event.preventDefault();
                $event.stopPropagation();
                scope.openedStart = true;
            }
            scope.openEnd = function ($event) {
                $event.preventDefault();
                $event.stopPropagation();
                scope.openedEnd = true;
            }
            scope.dateOptions = {
                formatYear: 'yy',
                startingDay: 1
            };
        }
    }
});