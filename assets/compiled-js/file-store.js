// Generated by CoffeeScript 1.6.3
(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  module("ashtag");

  ashtag.FileStore = (function() {
    function FileStore() {
      this._handleStoreFailure = __bind(this._handleStoreFailure, this);
      this._handleStoreSuccess = __bind(this._handleStoreSuccess, this);
      this._storeFile = __bind(this._storeFile, this);
      this.imageFieldName = "image";
      this.enabled = this._supported();
      ashtag.lib.mixins.Observable.prototype.augment(this);
      if (!this._supported) {
        return;
      }
      this.db = this.getDb();
      this.initialiseDb();
      this.allToServer();
    }

    FileStore.prototype._supported = function() {
      return !!window.openDatabase;
    };

    FileStore.prototype.disable = function() {
      this.enabled = false;
      return this.fire('disable');
    };

    FileStore.prototype.enable = function() {
      this.enabled = true;
      return this.fire('enable');
    };

    FileStore.prototype.getDb = function() {
      return window.openDatabase('uploader', '', 'Pending uploads', 10 * 1024 * 1024);
    };

    FileStore.prototype.initialiseDb = function() {
      var _this = this;
      return this.query("CREATE TABLE IF NOT EXISTS [files] (                     [id] INTEGER PRIMARY KEY AUTOINCREMENT,                    [name], [meta], [file]                )").then(function() {
        return _this.enable();
      }, function() {
        return _this.disable();
      });
    };

    FileStore.prototype.storeFile = function(file, meta) {
      if (meta == null) {
        meta = '';
      }
      if (!this.enabled) {
        throw 'Offline uploading disabled';
      }
      return this._readFile(file, meta).then(this._storeFile).then(this._handleStoreSuccess, this._handleStoreFailure);
    };

    FileStore.prototype._readFile = function(file, meta) {
      var deferred, reader,
        _this = this;
      deferred = $.Deferred();
      reader = new FileReader();
      reader.onloadend = function(e) {
        var fileData;
        fileData = e.target.result;
        return deferred.resolve(file.name, fileData, meta);
      };
      reader.readAsDataURL(file);
      return deferred.promise();
    };

    FileStore.prototype._storeFile = function(fileName, fileData, meta) {
      var deferred;
      deferred = $.Deferred();
      this.query("INSERT INTO [files] ([name], [meta], [file]) VALUES (?, ?, ?)", [fileName, meta, fileData]).then(function() {
        return deferred.resolve();
      }, function() {
        return deferred.reject();
      });
      return deferred.promise();
    };

    FileStore.prototype._handleStoreSuccess = function() {};

    FileStore.prototype._handleStoreFailure = function() {};

    FileStore.prototype.allToServer = function() {
      var deferred,
        _this = this;
      deferred = $.Deferred();
      this.query("SELECT * FROM [files]").then(function(rows) {
        var send;
        send = function() {
          var row;
          row = rows.pop();
          if (row) {
            return _this.popToServer(row).then(function() {
              return deferred.notify();
            });
          } else {
            return deferred.resolve();
          }
        };
        deferred.then(null, null, send);
        return send();
      });
      return deferred.promise();
    };

    FileStore.prototype.popToServer = function(row) {
      var deferred,
        _this = this;
      deferred = $.Deferred();
      this.sendRequest(row.name, row.file, row.meta).then(function() {
        return _this.query("DELETE FROM [files] WHERE [id] = ?", [row.id]).then(function() {
          return deferred.resolve();
        }, function() {
          return deferred.resolve();
        });
      }, function() {
        return deferred.resolve();
      });
      return deferred.promise();
    };

    FileStore.prototype.sendRequest = function(name, file, meta) {
      var data;
      data = ["" + this.imageFieldName + "_name=" + name, "" + this.imageFieldName + "=" + file];
      if (meta) {
        data.push(meta);
      }
      return $.ajax({
        data: data.join('&'),
        type: 'POST'
      });
    };

    FileStore.prototype.query = function(sql, values) {
      var deferred,
        _this = this;
      if (values == null) {
        values = [];
      }
      deferred = $.Deferred();
      this.db.transaction(function(tx) {
        return tx.executeSql(sql, values, function(tx, res) {
          var rows;
          rows = [];
          while (rows.length < res.rows.length) {
            rows.push(res.rows.item(rows.length));
          }
          return deferred.resolve(rows);
        });
      });
      return deferred.promise();
    };

    return FileStore;

  })();

}).call(this);
