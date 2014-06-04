$window = $(window);
var trackApp = angular.module('trackApp', [
    'ngRoute',
    'tracktastic',
    'd3'
]);

trackApp.config(['$routeProvider',
    function ($routeProvider) {
        $routeProvider.
            when('/processes', {
                templateUrl: 'partials/process-list.html',
                controller: 'TracktasticCtrl'
            })
//        .
//      when('/processes/:phoneId', {
//        templateUrl: 'partials/phone-detail.html',
//        controller: 'PhoneDetailCtrl'
//      }).
            .otherwise({
                redirectTo: '/processes'
            });
    }]);


trackApp.directive('d3Process', ['d3Service', function (d3Service) {
    return {
         restrict: 'EA',
         scope: {
             data:'=',
             onClick:'&',
             test:'='
         },
         link: function (scope, element, attrs) {
             d3Service.d3().then(function (d3) {
                 var margin = parseInt(attrs.margin) || 20,
                    barHeight = parseInt(attrs.barHeight) || 30,
                    barPadding = parseInt(attrs.barPadding) || 5;
                 var svg = d3.select(element[0])
                    .append('svg')
                    .style('width', '100%');
                 svg.attr('height', "100px");

                 // Browser onresize event
                window.onresize = function () {
                    scope.$apply();
                };
                 scope.$watch('data', function(newVals, oldVals) {
                   console.log("NEW PROCESSES");
                  return scope.renderProcesses(newVals);
                }, true);



                scope.renderProcesses = function(data) {
//                    console.log(data);

                    svg.selectAll('*').remove();

                    // If we don't pass any data, return out of the element
                    if (!data) return;

                    first = data[0]
                    last = data[data.length-1]
                    console.log(first);
                    var starttime = new Date(first.datetime).getTime();
                    var endtime = new Date(last.datetime).getTime();
                    console.log(starttime);
                    console.log(endtime);


                    var width = d3.select(element[0]).node().offsetWidth - margin,

                    color = d3.scale.category20();

//                    xScale = d3.scale.linear()
//                            .domain([d3.min(data, function (d) {
//                                return new Date(d.datetime).getTime();
//                            }),
//                            d3.max(data, function (d) {
//                                return new Date(d.datetime).getTime();
//                            })
//
//                        ])
//                            .range([0, width]);
                    xScale = d3.scale.linear()
                        .domain([0,endtime-starttime])
                        .range([0,width])


                    var lasttime = 0;
                    svg.selectAll('rect')
                        .data(data).enter()
                        .append('rect')
                        .attr('height', barHeight)
//                        .attr('width', 140)
                        .attr('x', function(d,i){
//                            return xScale(lasttime);
                            if (i != 0) {
                                var lastD = data[i-1];
                                var lasttime = new Date(lastD.datetime).getTime()
                                return  xScale(lasttime - starttime);
                            } else {
                                return 0;
                            }
                        })
//                        .attr('x',xScale(lasttime))
                        .attr('y', function (d, i) {
                            return 0;
                            return i * (barHeight + barPadding);
                        })
                        .on('click',function(d,i) {
                            console.log(d);
                            scope.test();
                            return scope.onClick({item: d});
                        })
                        .attr('fill', function (d) {
                            return color(d.process_type.id);
                        })
//                        .transition()
//                        .duration(1000)
                        .attr('width', function (d,i) {

                            var timediff = new Date(d.datetime).getTime();

                            if (i != 0) {
                                var lastD = data[i-1];
                                var lasttime = new Date(lastD.datetime).getTime()

                                return  xScale(timediff - lasttime);
                            } else {
                                return xScale(timediff);
                            }

//                            lasttime = new Date(d.datetime).getTime();

                            lasttime = timediff
//                            console.log(xScale(lasttime))
//                            return 100;

                        });

                    console.log(xScale(lasttime));

                }
             });
         }
    }
}]);
trackApp.directive('d3Barsxx', ['d3Service', function (d3Service) {
    return {
        restrict: 'EA',
        scope: {data:'='},
        link: function (scope, element, attrs) {
            d3Service.d3().then(function (d3) {
                var margin = parseInt(attrs.margin) || 20,
                    barHeight = parseInt(attrs.barHeight) || 30,
                    barPadding = parseInt(attrs.barPadding) || 5;
                var svg = d3.select(element[0])
                    .append('svg')
                    .style('width', '100%');

                // Browser onresize event
                window.onresize = function () {
                    scope.$apply();
                };

                // hard-code data
//                scope.data = [
//                    {name: "Greg", score: 18},
//                    {name: "Ari", score: 96},
//                    {name: 'Q', score: 75},
//                    {name: "Loser", score: 48}
//                ];

                // Watch for resize event
                scope.$watch(function () {
                    return angular.element($window)[0].innerWidth;
                }, function () {
                    scope.render(scope.data);
                });

                scope.$watch('data', function(newVals, oldVals) {
                   console.log("NEW DATA");
                   console.log(newVals);
                  return scope.render(newVals);
                }, true);


                scope.render = function (data) {
                    // remove all previous items before render
                    svg.selectAll('*').remove();

                    // If we don't pass any data, return out of the element
                    if (!data) return;

                    // setup variables
                    var width = d3.select(element[0]).node().offsetWidth - margin,
                    // calculate the height
                        height = scope.data.length * (barHeight + barPadding),
                    // Use the category20() scale function for multicolor support
                        color = d3.scale.category20(),
                    // our xScale
                        xScale = d3.scale.linear()
                            .domain([0, d3.max(data, function (d) {
                                return d.score;
                            })])
                            .range([0, width]);

                    // set the height based on the calculations above
                    svg.attr('height', height);

                    //create the rectangles for the bar chart
                    svg.selectAll('rect')
                        .data(data).enter()
                        .append('rect')
                        .attr('height', barHeight)
                        .attr('width', 140)
                        .attr('x', Math.round(margin / 2))
                        .attr('y', function (d, i) {
                            return i * (barHeight + barPadding);
                        })
                        .attr('fill', function (d) {
                            return color(d.score);
                        })
                        .transition()
                        .duration(1000)
                        .attr('width', function (d) {
                            return xScale(d.score);
                        });
                }
            });
        }};
}]);