// Generated by CoffeeScript 1.6.3
(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  module("ashtag");

  ashtag.FileStore = (function() {
    function FileStore() {
      this._handleStoreFailure = __bind(this._handleStoreFailure, this);
      this._handleStoreSuccess = __bind(this._handleStoreSuccess, this);
      this._storeFile = __bind(this._storeFile, this);
      this._resizeFile = __bind(this._resizeFile, this);
      this.imageFieldName = "image";
      this.imageMaxWidth = 800;
      this.imageMaxHeight = 600;
      this.enabled = this._supported();
      ashtag.lib.mixins.Observable.prototype.augment(this);
      if (!this.enabled) {
        return;
      }
      this.initialiseDb();
    }

    FileStore.prototype._supported = function() {
      return false;
      return !!window.openDatabase;
    };

    FileStore.prototype.disable = function() {
      this.enabled = false;
      return this.fire('disable');
    };

    FileStore.prototype.enable = function() {
      this.enabled = true;
      this.initialiseDb();
      return this.fire('enable');
    };

    FileStore.prototype.getDb = function() {
      return window.openDatabase('uploader', '', 'Pending uploads', 5 * 1024 * 1024);
    };

    FileStore.prototype.initialiseDb = function() {
      var _this = this;
      this.db = this.getDb();
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
      return this._readFile(file, meta).then(this._resizeFile).then(this._storeFile).then(this._handleStoreSuccess, this._handleStoreFailure);
    };

    FileStore.prototype._readFile = function(file, meta) {
      var deferred, reader,
        _this = this;
      deferred = $.Deferred();
      reader = new FileReader();
      reader.onloadend = function(e) {
        return deferred.resolve(file, reader, meta);
      };
      reader.readAsDataURL(file);
      return deferred.promise();
    };

    FileStore.prototype._resizeFile = function(file, reader, meta) {
      var canvas, def, handleLoaded, img, interval,
        _this = this;
      def = $.Deferred();
      canvas = document.createElement("canvas");
      img = new Image();
      handleLoaded = function() {
        var ctx, height, resizedData, width;
        ctx = canvas.getContext("2d");
        ctx.drawImage(img, 0, 0);
        width = img.width;
        height = img.height;
        if (width > height) {
          if (width > _this.imageMaxWidth) {
            height *= _this.imageMaxWidth / width;
            width = _this.imageMaxWidth;
          }
        } else {
          if (height > _this.imageMaxHeight) {
            width *= _this.imageMaxHeight / height;
            height = _this.imageMaxHeight;
          }
        }
        canvas.width = width;
        canvas.height = height;
        ctx = canvas.getContext("2d");
        ctx.drawImage(img, 0, 0, width, height);
        resizedData = canvas.toDataURL("image/jpeg");
        return def.resolve(file, resizedData, meta);
      };
      img.src = reader.result;
      interval = setInterval(function() {
        console.log(img.width);
        if (img.width > 0) {
          handleLoaded();
          return clearInterval(interval);
        }
      }, 100);
      return def;
    };

    FileStore.prototype._storeFile = function(file, fileData, meta) {
      var deferred;
      deferred = $.Deferred();
      this.query("INSERT INTO [files] ([name], [meta], [file]) VALUES (?, ?, ?)", [file.name, meta, fileData]).then(function() {
        return deferred.resolve();
      }, function() {
        return deferred.reject();
      });
      return deferred.promise();
    };

    FileStore.prototype._handleStoreSuccess = function() {
      return this.allToServer();
    };

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
      data = [("" + this.imageFieldName + "_name=") + encodeURIComponent(name), ("" + this.imageFieldName + "=") + encodeURIComponent(file)];
      if (meta) {
        data.push(meta);
      }
      return $.ajax({
        url: window.location.pathname,
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

    FileStore.prototype.totalPendingFiles = function() {
      var deferred;
      deferred = $.Deferred();
      this.query('SELECT COUNT(*) AS count FROM [files]').then(function(rows) {
        return deferred.resolve(rows[0].count);
      });
      return deferred.promise();
    };

    return FileStore;

  })();

}).call(this);
