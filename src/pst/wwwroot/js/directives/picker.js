angular.module('trackApp')
    .directive('picker', ['$cookieStore', function ($cookieStore) {
        return {
            link: function (scope, element, attrs) {


                scope.pickerStartTime = new Date($cookieStore.get('startdate'));

                console.log(scope.pickerStartTime);
                if (angular.isUndefined(scope.pickerStartTime)) {
                    scope.pickerStartTime = new Date();
                    scope.pickerStartTime.setUTCHours(0);
                    scope.pickerStartTime.setHours(9)
                    scope.pickerStartTime.setMinutes(0)
                    scope.pickerStartTime.setSeconds(0);
                }

                scope.pickerEndTime = new Date($cookieStore.get('enddate'));

                if (angular.isUndefined(scope.pickerEndTime)) {
                    scope.pickerEndTime = new Date();
                    scope.pickerEndTime.setUTCHours(0);
                    scope.pickerEndTime.setHours(23);
                    scope.pickerEndTime.setMinutes(59);
                }

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

                getWorkingDay = function() {
                    var start = new Date()
                        start.setHours(9);
                        start.setMinutes(0);
                        start.setSeconds(0);
                        start.setMilliseconds(0);
                        var end = new Date()
                        end.setHours(18);
                        end.setMinutes(0);
                        end.setSeconds(0);
                        end.setMilliseconds(0);
                        return [start,end];
                }
                getLastHours = function(hours) {
                    var start = new Date().addHours(-hours);
                    var end = new Date();
                    return [start,end];
                }

                scope.quickChoices = [
                    {
                        title: "Today",
                        func: function () {
                            return getWorkingDay()
                        }
                    },
                    {
                        title: "Yesterday",
                        func: function () {
                            var day = getWorkingDay();
                            day[0].addHours(-24);
                            day[1].addHours(-24);
                            return day;
                        }
                    },
                    {
                        title: "Last Hour",
                        func: function () {
                            return getLastHours(1);
                        }
                    }
                ];

                scope.quickChoiceChosen = function(item) {
                    result = item.func();
                    scope.pickerStartTime = result[0];
                    scope.pickerEndTime = result[1];
                }
            }
        }
    }]);