describe('PhoneCat App', function() {

  describe('Phone list view', function() {

    beforeEach(function() {
      browser.get('index.html');
    });
    it('should filter the phone list as user types into the search box', function() {

      var phoneList = element.all(by.repeater('process in processes'));
      var query = element(by.model('query'));

      expect(phoneList.count()).toBeGreaterThan(0);

//      query.sendKeys('nexus');
//      expect(phoneList.count()).toBe(1);
//
//      query.clear();
//      query.sendKeys('motorola');
//      expect(phoneList.count()).toBe(2);
    });

//    it('should display the current filter value in the title bar', function() {
//
//    expect(browser.getTitle()).toMatch(/Google Phone Gallery:\s*$/);
//
//    element(by.model('query')).sendKeys('nexus');
//
//    expect(browser.getTitle()).toMatch(/Google Phone Gallery: nexus$/);
//  });

//      it('should be possible to control phone order via the drop down select box', function() {
//
//      var phoneNameColumn = element.all(by.repeater('process in processes').column('{{process.title}}'));
//      var query = element(by.model('query'));
//
//      function getNames() {
//        return phoneNameColumn.map(function(elm) {
//          return elm.getText();
//        });
//      }
//
//      query.sendKeys('tablet'); //let's narrow the dataset to make the test assertions shorter
//
//      expect(getNames()).toEqual([
//        "Motorola XOOM with Wi-Fi",
//        "MOTOROLA XOOM"
//      ]);
//
//      element(by.model('orderProp')).findElement(by.css('option[value="title"]')).click();
//
//      expect(getNames()).toEqual([
//        "MOTOROLA XOOM",
//        "Motorola XOOM with Wi-Fi"
//      ]);
//    });

  });
});