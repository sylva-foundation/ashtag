// Generated by CoffeeScript 1.6.3
(function() {
  var _ref,
    __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  module("ashtag.panes");

  ashtag.panes.SubmitSightingMapPane = (function(_super) {
    __extends(SubmitSightingMapPane, _super);

    function SubmitSightingMapPane() {
      this.handleMapLoad = __bind(this.handleMapLoad, this);
      this.handleDragEnd = __bind(this.handleDragEnd, this);
      _ref = SubmitSightingMapPane.__super__.constructor.apply(this, arguments);
      return _ref;
    }

    SubmitSightingMapPane.prototype.initialise = function() {
      var loc;
      SubmitSightingMapPane.__super__.initialise.apply(this, arguments);
      this.$locationInput = $('#id_location');
      loc = this.parseLocation();
      if (loc) {
        this.defaultLat = loc.lat;
        this.defaultLng = loc.lng;
        return this.defaultZoom = 19;
      }
    };

    SubmitSightingMapPane.prototype.parseLocation = function() {
      var match, re, text;
      text = this.$locationInput.val();
      if (!text) {
        return;
      }
      re = /^POINT\s*\(([-\.\d]+) ([-\.\d]+)\)$/g;
      match = re.exec(text);
      return {
        lat: parseFloat(match[2], 10),
        lng: parseFloat(match[1], 10)
      };
    };

    SubmitSightingMapPane.prototype.createMarker = function() {
      var marker;
      marker = new google.maps.Marker({
        position: new google.maps.LatLng(this.defaultLat, this.defaultLng),
        draggable: true,
        bounds: false,
        map: this.map
      });
      google.maps.event.addDomListener(marker, 'dragend', this.handleDragEnd);
      return this.updateLocation(this.defaultLat, this.defaultLng);
    };

    SubmitSightingMapPane.prototype.handleDragEnd = function(e) {
      return this.updateLocation(e.latLng.lat(), e.latLng.lng());
    };

    SubmitSightingMapPane.prototype.updateLocation = function(lat, lng) {
      return this.$locationInput.val("POINT (" + lng + " " + lat + ")");
    };

    SubmitSightingMapPane.prototype.handleMapLoad = function() {
      SubmitSightingMapPane.__super__.handleMapLoad.apply(this, arguments);
      return this.createMarker();
    };

    return SubmitSightingMapPane;

  })(ashtag.panes.MapBasePane);

}).call(this);
