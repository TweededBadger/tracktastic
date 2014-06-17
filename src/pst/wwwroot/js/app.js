$window = $(window);
var trackApp = angular.module('trackApp', [
    'ngRoute',
    'tracktastic',
    'd3',
    'ui.bootstrap',
    'ui.sortable'
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
             test:'&',
             redraw:'=',
             startTime:'=',
             endTime:'='
         },
         link: function (scope, element, attrs) {
             d3Service.d3().then(function (d3) {
                 var margin = parseInt(attrs.margin) || 20,
                    barHeight = parseInt(attrs.barHeight) || 30,
                    barPadding = parseInt(attrs.barPadding) || 5;
                 var svg = d3.select(element[0])
                    .append('svg')
                    .style('width', '100%');
                 var maxy = -1;
                 svg.attr('height', "0px");

                 var starttime = scope.startTime;
                 var endtime = scope.endTime;
//                 var starttime = new Date().getTime();
//                 var endtime = new Date().getTime();
                 var color = d3.scale.category20();

                 // Browser onresize event
                window.onresize = function () {
                    scope.$apply();
                };
                 scope.$watch('redraw', function(newVals, oldVals) {
                        console.log("redraw "+scope.redraw);
                     if (scope.redraw) {
                         console.log("do redraw");
                         scope.redraw = false;
                         return scope.renderProcesses(scope.data);
                     }
                }, true);

                drawProcess = function(data,category) {
                    svg.append('rect')
                        .attr('height', barHeight)
//                        .attr('width', 140)
                        .attr('x', function(){
                            var start = new Date(data.start_time).getTime();
                            return xScale(start)
                        })
                        .attr('y', function () {
//                            return 0;
                            var yval = category.id * (barHeight + barPadding);
                            if (yval > maxy) {
                                maxy = yval;
                                svg.attr('height', yval+barHeight);
                            }
                            return category.id * (barHeight + barPadding);

                        })
                        .on('mouseover',function() {
                            return scope.onClick({item: data});
                        })
                        .attr('fill', function () {
                            return color(category.id);
                        })
                        .attr('width', function () {
                            var start = new Date(data.start_time).getTime();
                            var end = new Date(data.end_time).getTime();
//                            return  xScale(end - start);
                            var duration = end-start;
                            console.log(duration)
                            console.log(xScale(duration + starttime.getTime()))
                            return  xScale(duration + starttime.getTime())
//                            return 1;
                        });
                }

                scope.renderProcesses = function(data) {
//                    console.log(data);

                    svg.selectAll('*').remove();

                    starttime = scope.startTime;
                    endtime = scope.endTime;

                    // If we don't pass any data, return out of the element
                    if (!data) return;
                    first = data[0]
                    last = data[data.length-1]
//                    starttime = new Date(first.start_time).getTime();
//                    endtime = new Date(last.end_time).getTime();
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
                        .domain([starttime.getTime(),endtime.getTime()])
                        .range([0,width])

                    angular.forEach(data,function(process,key){
                        angular.forEach(process.process_categories,function(pcat,key){
                            drawProcess(process,pcat)
                        });
                    });
//                    svg.selectAll('rect')
//                        .data(data).enter()
//                        .append('rect')
//                        .attr('height', barHeight)
////                        .attr('width', 140)
//                        .attr('x', function(d,i){
//                            var start = new Date(d.start_time).getTime();
//                            return xScale(start - starttime)
//                        })
//                        .attr('y', function (d, i) {
////                            return 0;
//                            var yval = d.process_category.id * (barHeight + barPadding);
//                            if (yval > maxy) {
//                                maxy = yval;
//                                svg.attr('height', yval+barHeight);
//                            }
//                            return d.process_category.id * (barHeight + barPadding);
//
//                        })
//                        .on('mouseover',function(d,i) {
//                            return scope.onClick({item: d});
//                        })
//                        .attr('fill', function (d) {
//                            return color(d.process_category.id);
//                        })
//                        .attr('width', function (d,i) {
//
//                            var start = new Date(d.start_time).getTime();
//                            var end = new Date(d.end_time).getTime();
//                            return  xScale(end - start);
//                        });


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