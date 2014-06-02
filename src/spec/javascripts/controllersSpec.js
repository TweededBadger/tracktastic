
describe('TracktasticCtrl', function(){
    var scope,ctrl, $httpBackend;

  beforeEach(module('tracktastic'));

    // The injector ignores leading and trailing underscores here (i.e. _$httpBackend_).
    // This allows us to inject a service but then attach it to a variable
    // with the same name as the service in order to avoid a name conflict.
    beforeEach(inject(function(_$httpBackend_, $rootScope, $controller) {
      $httpBackend = _$httpBackend_;
      $httpBackend.expectGET('data/processes/').
          respond([{title: 'Nexus S'}, {title: 'Motorola DROID'}]);

      scope = $rootScope.$new();
      ctrl = $controller('TracktasticCtrl', {$scope: scope});
    }));

  it('should create "phones" model with 2 phones fetched from xhr', function() {
      expect(scope.processes).toBeUndefined();
      $httpBackend.flush();
      expect(scope.processes).toEqual([{title: 'Nexus S'},
                                   {title: 'Motorola DROID'}]);
    });

    it('should set the default value of orderProp model', function() {
      expect(scope.orderProp).toBe('age');
    });

});



//describe('TracktasticCtrl', function(){
//
//  beforeEach(angular.module('tracktastic'));
//
//  it('should create "phones" model with 3 phones', inject(function($controller) {
//    var scope = {},
//        ctrl = $controller('TracktasticCtrl', {$scope:scope});
//
//    expect(scope.phones.length).toBe(3);
//  }));
//
//});

//
//describe("A suite is just a function", function() {
//  var a;
//
//  it("and so is a spec", function() {
//    a = true;
//
//    expect(a).toBe(true);
//  });
//});
//
//describe("A spec (with setup and tear-down)", function() {
//  var foo;
//
//  beforeEach(function() {
//    foo = 0;
//    foo += 1;
//  });
//
//  afterEach(function() {
//    foo = 0;
//  });
//
//  it("is just a function, so it can contain any code", function() {
//    expect(foo).toEqual(1);
//  });
//
//  it("can have more than one expectation", function() {
//    expect(foo).toEqual(1);
//    expect(true).toEqual(true);
//  });
//});