(function() {
  var _ref,
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  module("ashtag.panes");

  ashtag.panes.BuyTagsPane = (function(_super) {
    __extends(BuyTagsPane, _super);

    function BuyTagsPane() {
      _ref = BuyTagsPane.__super__.constructor.apply(this, arguments);
      return _ref;
    }

    BuyTagsPane.prototype.setupEvents = function() {
      return console.log('BuyTagsPane');
    };

    BuyTagsPane.prototype.start = function() {};

    return BuyTagsPane;

  })(ashtag.lib.panes.BasePane);

  if ($('#buy-tags-page').length) {
    new ashtag.panes.BuyTagsPane($('#buy-tags-page'));
  }

}).call(this);
