(function() {
  var _ref,
    __indexOf = [].indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; },
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
    __slice = [].slice;

  module("ashtag.lib.mixins");

  ashtag.lib.mixins.Mixin = (function() {
    function Mixin() {}

    Mixin.prototype.augment = function(t) {
      var m, n;
      for (n in this) {
        m = this[n];
        if (!(n === 'augment' || n === 'eject' || n === 'setupMixin' || n === 'constructor' || (this[n].prototype == null))) {
          t[n] = m;
        }
      }
      return this.setupMixin.call(t);
    };

    Mixin.prototype.eject = function(mixin) {
      var m, n, o, p, _results;
      _results = [];
      for (n in this) {
        m = this[n];
        _results.push(__indexOf.call((function() {
          var _ref, _results1;
          _ref = mixin.prototype;
          _results1 = [];
          for (o in _ref) {
            p = _ref[o];
            _results1.push(p);
          }
          return _results1;
        })(), m) >= 0 ? delete this[n] : void 0);
      }
      return _results;
    };

    Mixin.prototype.setupMixin = function() {};

    return Mixin;

  })();

  ashtag.lib.mixins.Observable = (function(_super) {
    __extends(Observable, _super);

    function Observable() {
      _ref = Observable.__super__.constructor.apply(this, arguments);
      return _ref;
    }

    Observable.eventNamesMatch = function(eventMasks, eventName) {
      var eventMask, isOpenEnded, isOpenFronted, _i, _len;
      if (typeof eventMasks !== "object") {
        eventMasks = [eventMasks];
      }
      for (_i = 0, _len = eventMasks.length; _i < _len; _i++) {
        eventMask = eventMasks[_i];
        if (eventMask === eventName) {
          return eventMask;
        }
        if (eventMask === "*") {
          return eventMask;
        }
        isOpenEnded = eventMask[eventMask.length - 1] === ".";
        if (isOpenEnded && eventName.substr(0, eventMask.length) === eventMask) {
          return eventMask;
        }
        isOpenFronted = eventMask[0] === ".";
        if (isOpenFronted && eventName.substr(-eventMask.length) === eventMask) {
          return eventMask;
        }
      }
      return false;
    };

    Observable.prototype.setupMixin = function() {
      return this.registry = [];
    };

    Observable.prototype.observe = function(name, fn) {
      var item, _i, _len, _ref1;
      _ref1 = this.registry;
      for (_i = 0, _len = _ref1.length; _i < _len; _i++) {
        item = _ref1[_i];
        if (item.name === name && item.fn === fn) {
          return false;
        }
      }
      this.registry.push({
        name: name,
        fn: fn
      });
      return true;
    };

    Observable.prototype.unobserve = function(name, fn) {
      var k, v, _i, _len, _ref1, _results;
      _ref1 = this.registry;
      _results = [];
      for (k = _i = 0, _len = _ref1.length; _i < _len; k = ++_i) {
        v = _ref1[k];
        if (item.name === name && item.fn === fn) {
          _results.push(this.registry.splice(k, 1));
        }
      }
      return _results;
    };

    Observable.prototype.unobserveAll = function() {
      var k, v, _i, _len, _ref1;
      _ref1 = this.registry;
      for (k = _i = 0, _len = _ref1.length; _i < _len; k = ++_i) {
        v = _ref1[k];
        delete this.registry[k].name;
        delete this.registry[k].fn;
      }
      return this.registry = [];
    };

    Observable.prototype.unobserveAllBy = function(eventMask) {
      var k, v, _i, _len, _ref1, _results;
      _ref1 = this.registry;
      _results = [];
      for (k = _i = 0, _len = _ref1.length; _i < _len; k = ++_i) {
        v = _ref1[k];
        if (ashtag.Observable.eventNamesMatch(eventMask, v.name)) {
          this.registry.splice(k, 1);
          _results.push(k -= 1);
        } else {
          _results.push(void 0);
        }
      }
      return _results;
    };

    Observable.prototype.observeOnce = function(name, fn) {
      ({
        wrapper: function() {
          var params;
          params = 1 <= arguments.length ? __slice.call(arguments, 0) : [];
          this.unobserve(name, wrapper);
          return fn.apply(this, params);
        }
      });
      return this.observe(name, wrapper);
    };

    /*
    Fire an event which can be observed by observe()
    
    name - The name of the event
    data - An array of values that will be passed to the observing function as individual parameters
    scope - The scope in which the observing function will be called
    */


    Observable.prototype.fire = function() {
      var fn, fns, k, matchedBy, name, names, params, v, _i, _j, _len, _len1, _ref1, _results;
      name = arguments[0], params = 2 <= arguments.length ? __slice.call(arguments, 1) : [];
      fns = [];
      names = [];
      _ref1 = this.registry;
      for (_i = 0, _len = _ref1.length; _i < _len; _i++) {
        v = _ref1[_i];
        matchedBy = ashtag.lib.mixins.Observable.eventNamesMatch(name, v.name);
        if (matchedBy) {
          fns.push(v.fn);
          names.push(v.name);
        }
      }
      _results = [];
      for (k = _j = 0, _len1 = fns.length; _j < _len1; k = ++_j) {
        fn = fns[k];
        params.unshift({
          originalName: name,
          eventName: name,
          observingFor: names,
          matchedBy: matchedBy,
          data: params.slice(0)
        });
        _results.push(fn.apply(this, params));
      }
      return _results;
    };

    return Observable;

  })(ashtag.lib.mixins.Mixin);

}).call(this);