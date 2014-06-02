var processServices = angular.module('processServices',['ngResource']);

processServices.factory("Process",['$resource',
function($resource) {
    return $resource('http://127.0.0.1:8081/data/processes',{},{
        query: {method:'GET',params:{xxx:''},
        isArray:true}
    });
}]);