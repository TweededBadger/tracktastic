var tracktastic = angular.module('tracktastic', []);

tracktastic.controller('TracktasticCtrl',
    ['$scope', '$http',
        function ($scope, $http) {

            $scope.testfunc = function (data) {
                console.log(data);
                console.log("This test says hello");
            }

            $scope.trackClick = function (item) {
//                console.log(item);
                $scope.$apply(function () {
//                    console.log("CLICK");
                    if (!$scope.showDetailPanel)
                        $scope.showDetailPanel = true;
                    $scope.detailItem = item;
                });
            };

//            $http.get("data/processes/").success(function (data) {
//                $scope.processes = data;
//            })

            $scope.$watch('dt',function(oldValue,newValue){
                console.log("Date Picked: "+newValue);
                if (angular.isDefined($scope.dt)) {
                    processSearch($scope.dt);
                }
            });

            $scope.greeting = "Blah Blah Blah";
            $scope.data = [
                {name: "Greg", score: 2},
                {name: "Ari", score: 96},
                {name: 'Q', score: 75},
                {name: "Loser", score: 48}
            ];

            processSearch = function(start_time) {

                $http({
                    method:'GET',
                    url:'data/processes/',
                    params: {
                        start_time:start_time.toUTCString(),
                        end_time:start_time.addHours(24).toUTCString(),
                        test:"test"
                    }
                }).success(function(data){
                    console.log("------------1")
                    $scope.processes = data;
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