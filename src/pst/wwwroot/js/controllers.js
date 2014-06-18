var tracktastic = angular.module('tracktastic', []);

tracktastic.controller('TracktasticCtrl',
    ['$scope', '$http','$cookieStore',
        function ($scope, $http,$cookieStore) {

            $scope.trackClick = function (item,event) {
//                console.log(item);
                if (event.type == 'mouseout')
                {
                    $scope.$apply(function () {
                        $scope.showDetailPanel = false;
                    });
                }
                else {
                    $scope.detailsStyle = {
                        top: (event.pageY - 10) + "px",
                        left: (event.pageX + 10) + "px"
                    }
                    $scope.$apply(function () {
                        if (!$scope.showDetailPanel)
                            $scope.showDetailPanel = true;
                        $scope.detailItem = item;
                    });
                }
            };

//            $http.get("data/processes/").success(function (data) {
//                $scope.processes = data;
//            })

            $scope.$watch('pickerStartTime',function(oldValue,newValue){
                    $cookieStore.put('startdate',$scope.pickerStartTime);
                    processSearch($scope.pickerStartTime,$scope.pickerEndTime);
            });
            $scope.$watch('pickerEndTime',function(oldValue,newValue){
                    $cookieStore.put('enddate',$scope.pickerEndTime);
                    processSearch($scope.pickerStartTime,$scope.pickerEndTime);
            });

            $scope.convertDate = function(d) {
                return new Date(d);
            }

            $scope.greeting = "Blah Blah Blah";
            $scope.data = [
                {name: "Greg", score: 2},
                {name: "Ari", score: 96},
                {name: 'Q', score: 75},
                {name: "Loser", score: 48}
            ];
            $scope.redraw = true;
            $scope.viewableCategories = []

            processSearch = function(start_time,end_time) {
                if (angular.isUndefined(start_time) || angular.isUndefined(end_time)) return false;
                start_time_new = new Date(start_time.getTime()).addHours(1).toUTCString();
                end_time_new = new Date(start_time.getTime()).addHours(1).toUTCString();
                $http({
                    method:'GET',
                    url:'data/processes/',
                    params: {
                        start_time:new Date(start_time.getTime()).addHours(1).toUTCString(),
                        end_time:new Date(end_time.getTime()).addHours(1).toUTCString(),
                        random:Math.random()
                    }
                }).success(function(data){
                    $scope.processes = data;
                    $scope.redraw = true;
                })
            }


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

tracktastic.controller("TestCtrl",
    ['$scope', function ($scope) {
        $scope.greeting = "Blah Blah Blah";
        $scope.data = [
            {name: "Greg", score: 58},
            {name: "Ari", score: 96},
            {name: 'Q', score: 75},
            {name: "Loser", score: 48}
        ];
    }]);

angular.module('d3', [])
    .factory('d3Service', ['$document', '$q', '$rootScope',
        function ($document, $q, $rootScope) {
            var d = $q.defer();

            function onScriptLoad() {
                // Load client in the browser
                $rootScope.$apply(function () {
                    d.resolve(window.d3);
                });
            }

            // Create a script tag with d3 as the source
            // and call our onScriptLoad callback when it
            // has been loaded
            var scriptTag = $document[0].createElement('script');
            scriptTag.type = 'text/javascript';
            scriptTag.async = true;
            scriptTag.src = 'http://d3js.org/d3.v3.min.js';
            scriptTag.onreadystatechange = function () {
                if (this.readyState == 'complete') onScriptLoad();
            }
            scriptTag.onload = onScriptLoad;

            var s = $document[0].getElementsByTagName('body')[0];
            s.appendChild(scriptTag);

            return {
                d3: function () {
                    return d.promise;
                }
            };
        }]);