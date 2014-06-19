var tracktastic = angular.module('tracktastic', []);

tracktastic.controller('TracktasticCtrl',
    ['$scope', '$http', '$cookieStore','$modal',
        function ($scope, $http, $cookieStore,$modal) {

            $scope.trackClick = function (item, event) {
                $scope.detailItem = item;
                switch (event.type) {
                    case "mouseout":
                        $scope.$apply(function () {
                            $scope.showDetailPanel = false;
                        });
                        break;
                    case "mouseover":
                        $scope.detailsStyle = {
                            top: (event.pageY - 10) + "px",
                            left: (event.pageX + 10) + "px"
                        }
                        $scope.$apply(function () {
                            if (!$scope.showDetailPanel)
                                $scope.showDetailPanel = true;
                            $scope.detailItem = item;
                        });
                        break;
                    case "contextmenu":
                        $scope.$apply(function () {
                            $scope.showDetailPanel = false;
                            $scope.showContextPanel = true;
                             $scope.processContextStyle = {
                                top: (event.pageY - 10) + "px",
                                left: (event.pageX + 10) + "px"
                            }
                        });
                        break;
                }
            };

            $scope.deleteProcess = function() {
//                alert("Delete "+$scope.detailItem.title);
                var modalInstance = $modal.open({
                  templateUrl: 'partials/decision-model.html',
                  controller: ModalInstanceCtrl,
//                  size: size,
                  resolve: {
                    items: function () {
                      return $scope.items;
                    }
                  }
                });

                modalInstance.result.then(function (result) {
                  alert(result);
                }, function () {
                  $log.info('Modal dismissed at: ' + new Date());
                });
            }

            $scope.$watch('pickerStartTime', function (oldValue, newValue) {
                if (angular.isUndefined($scope.pickerStartTime)) return false;
                $cookieStore.put('startdate', $scope.pickerStartTime.toUTCString());
                processSearch($scope.pickerStartTime, $scope.pickerEndTime);
            });
            $scope.$watch('pickerEndTime', function (oldValue, newValue) {
                if (angular.isUndefined($scope.pickerEndTime)) return false;
                $cookieStore.put('enddate', $scope.pickerEndTime.toUTCString());
                processSearch($scope.pickerStartTime, $scope.pickerEndTime);
            });

            $scope.convertDate = function (d) {
                return new Date(d);
            }

            $scope.redraw = true;
            $scope.viewableCategories = []

            processSearch = function (start_time, end_time) {
                if (angular.isUndefined(start_time) || angular.isUndefined(end_time)) return false;
                start_time_new = new Date(start_time.getTime()).addHours(1).toUTCString();
                end_time_new = new Date(start_time.getTime()).addHours(1).toUTCString();
                $http({
                    method: 'GET',
                    url: 'data/processes/',
                    params: {
                        start_time: new Date(start_time.getTime()).addHours(1).toUTCString(),
                        end_time: new Date(end_time.getTime()).addHours(1).toUTCString(),
                        random: Math.random()
                    }
                }).success(function (data) {
                    $scope.processes = data;
                    $scope.redraw = true;
                })
            }
        }]);


var ModalInstanceCtrl = function ($scope, $modalInstance) {
//tracktastic.controller('ModalInstanceCtrl',
//    ['$scope','$modalInstance',
//        function ($scope, $modalInstance) {
            $scope.ok = function () {
                $modalInstance.close(true);
              };

              $scope.cancel = function () {
                $modalInstance.dismiss('cancel');
              };
        }
//]);


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
            scriptTag.src = 'js/d3.v3.min.js';
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