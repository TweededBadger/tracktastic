$window = $(window);
var trackApp = angular.module('trackApp', [
    'ngRoute',
    'ngCookies',
    'tracktastic',
    'd3',
    'ui.bootstrap',
    'ui.sortable'
]);

trackApp.config(['$routeProvider',
    function ($routeProvider) {
        $routeProvider.
            when('/processes', {
                templateUrl: 'partials/process-list.html'
            }).
            when('/categories', {
                templateUrl: 'partials/category-list.html'
            })
            .otherwise({
                redirectTo: '/processes'
            });
    }]);


trackApp.directive('d3Process', ['d3Service','$filter', function (d3Service,$filter) {
    return {
         restrict: 'EA',
         scope: {
             data:'=',
             onClick:'&',
             test:'&',
             redraw:'=',
             startTime:'=',
             endTime:'=',
             viewableCategories:'='
         },
         link: function (scope, element, attrs) {
             d3Service.d3().then(function (d3) {
                 var margin = parseInt(attrs.margin) || 20,
                    barHeight = parseInt(attrs.barHeight) || 30,
                    barPadding = parseInt(attrs.barPadding) || 5,
                     topMargin = 30;
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
                 scope.viewableCategories = [];
                 var totalProcessTime = 0;
                 // Browser onresize event
                window.onresize = function () {
                    scope.$apply();
                };
                 scope.$watch('redraw', function(newVals, oldVals) {
                     if (scope.redraw) {
                         scope.redraw = false;
                         return scope.renderProcesses(scope.data);
                     }
                }, true);

                drawProcess = function(data,category) {

                    pos = scope.viewableCategories.map(function(e) { return e.id; }).indexOf(category.id);

                    svg.append('rect')
                        .attr('height', barHeight)
//                        .attr('width', 140)
                        .attr('x', function(){
                            var start = new Date(data.start_time).getTime();
                            return xScale(start)
                        })
                        .attr('y', function () {
//                            return 0;
                            return (category.order * (barHeight + barPadding))+barPadding + topMargin;
                        })
                        .on('mouseover',function() {
                            return scope.onClick({item: data, event:event});
                        })
                        .on('mouseout',function() {
                            return scope.onClick({item: data, event:event});
                        })
                        .on('contextmenu',function() {
                            d3.event.preventDefault();
                            return scope.onClick({item: data, event:event});
                        })
                        .attr('fill', function () {
                            return color(category.id);
                        })
                        .attr('width', function () {
                            var start = new Date(data.start_time).getTime();
                            var end = new Date(data.end_time).getTime();
//                            return  xScale(end - start);
                            var duration = end-start;
                            return  xScale(duration + starttime.getTime())
//                            return 1;
                        });
                }

                 drawLabels = function() {
                     angular.forEach(scope.viewableCategories,function(cat,key){
                        svg.append('text')
                            .attr('x', function(){
                                return 0;
                            })
                            .attr('y', function(){
                                return ((cat.order) * (barHeight + barPadding))+barHeight/2 + topMargin;
                            })
                            .text(cat.title + " - " + $filter('date')(cat.totalTime,'HH:mm') + " - " +  $filter('number')((cat.totalTime/(endtime-starttime))*100,1) + "%")
                            .attr("font-family", "sans-serif")
                            .attr("font-size", "15px")
                            .attr("font-weight", "bold")
                            .attr("fill", color(cat.id));
                     })
                 }

                scope.renderProcesses = function(data) {

                    svg.selectAll('*').remove();
                    scope.viewableCategories = []
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
                    xScale = d3.time.scale()
                        .domain([starttime,endtime])
                        .range([0,width])

                    var xAxis = d3.svg.axis()
                        .scale(xScale)
                        .ticks(d3.time.hours)
                        .tickSize(1)
//                        .innerTickSize(1)
                        .orient("top");
                    height = 500;
                    var gx = svg.append("g")
                        .attr("class", "x axis")
                        .attr("transform", "translate(0,20)")
                        .call(xAxis);

                    svg.append("g")
                        .attr("class", "grid")
                        .attr("transform", "translate(0,20)")
                        .call(d3.svg.axis()
                            .scale(xScale)
                            .ticks(d3.time.hours)
                            .tickSize(height, 0, 0)
                            .tickFormat("")
                    )
                    angular.forEach(data,function(process,key){
                        angular.forEach(process.process_categories,function(pcat,key){
                            pos = scope.viewableCategories.map(function(e) { return e.id; }).indexOf(pcat.id);
                            if (pos == -1 ) {
                                pcat.totalTime = 0;
                                var i = scope.viewableCategories.push(pcat);
                                console.log(i);
                            }
                            pos = scope.viewableCategories.map(function(e) { return e.id; }).indexOf(pcat.id);
                            cat = scope.viewableCategories[pos];
                            var start = new Date(process.start_time).getTime();
                            var end = new Date(process.end_time).getTime();
                            cat.totalTime += (end-start);
                            drawProcess(process,pcat)
                        });
                    });
                    console.log(scope.viewableCategories);

                    svg.attr('height', scope.viewableCategories.length*(barHeight + barPadding) + topMargin);

                    drawLabels();

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