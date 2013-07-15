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
      ashtag.lib.mixins.Logging.prototype.augment(this);
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
      if (!window.uploaderDb) {
        window.uploaderDb = window.openDatabase('uploader', '', 'Pending uploads', 5 * 1024 * 1024);
        this.log('Creating and caching database connection');
      }
      return window.uploaderDb;
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
      if (typeof console !== "undefined" && console !== null) {
        if (typeof console.group === "function") {
          console.group('Storing file');
        }
      }
      return this._readFile(file, meta).then(this._resizeFile).then(this._storeFile).then(this._handleStoreSuccess, this._handleStoreFailure).then(function() {
        return console.groupEnd();
      }, function() {
        return console.groupEnd();
      });
    };

    FileStore.prototype._readFile = function(file, meta) {
      var deferred, reader,
        _this = this;
      this.log("Reading file");
      deferred = $.Deferred();
      reader = new FileReader();
      reader.onloadend = function(e) {
        _this.log("Reading complete");
        return deferred.resolve(file, reader, meta);
      };
      reader.readAsDataURL(file);
      return deferred.promise();
    };

    FileStore.prototype._resizeFile = function(file, reader, meta) {
      var canvas, def, handleLoaded, img, interval,
        _this = this;
      this.log("Resizing file");
      def = $.Deferred();
      canvas = document.createElement("canvas");
      img = new Image();
      handleLoaded = function() {
        var ctx, height, resizedData, width;
        _this.log('Image loaded. Calculating dimentions');
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
        _this.log("Resizing to " + width + " x " + height);
        ctx = canvas.getContext("2d");
        ctx.drawImage(img, 0, 0, width, height);
        _this.log("Getting image as encoded data");
        resizedData = canvas.toDataURL("image/jpeg");
        _this.log("Resize complete");
        return def.resolve(file, resizedData, meta);
      };
      img.src = reader.result;
      this.log('Waiting for image to load');
      interval = setInterval(function() {
        if (img.width > 0) {
          handleLoaded();
          return clearInterval(interval);
        }
      }, 100);
      return def;
    };

    FileStore.prototype._storeFile = function(file, fileData, meta) {
      var deferred,
        _this = this;
      this.log("Locally storing file with length " + fileData.length);
      deferred = $.Deferred();
      this.query("INSERT INTO [files] ([name], [meta], [file]) VALUES (?, ?, ?)", [file.name, meta, fileData]).then(function() {
        _this.log("Storing complete");
        return deferred.resolve();
      }, function() {
        _this.warn("Storing failed");
        return deferred.reject();
      });
      return deferred.promise();
    };

    FileStore.prototype._handleStoreSuccess = function() {
      this.log("File stored locally successfully");
      return this.allToServer();
    };

    FileStore.prototype._handleStoreFailure = function() {
      return this.warn("Local storage failed");
    };

    FileStore.prototype.allToServer = function() {
      var deferred,
        _this = this;
      this.log("Sending all locally stored files to the server");
      deferred = $.Deferred();
      this.query("SELECT * FROM [files]").then(function(rows) {
        var send;
        _this.log("Sending " + rows.length + " files");
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
      this.log("Popping file to the server");
      deferred = $.Deferred();
      this.sendRequest(row.name, row.file, row.meta).then(function() {
        _this.log("File sent, deleting from local db");
        return _this.query("DELETE FROM [files] WHERE [id] = ?", [row.id]).then(function() {
          _this.log("Deletion complete");
          return deferred.resolve();
        }, function() {
          _this.warn("Deletion failed");
          return deferred.resolve();
        });
      }, function() {
        return deferred.resolve();
      });
      return deferred.promise();
    };

    FileStore.prototype.sendRequest = function(name, file, meta) {
      var data,
        _this = this;
      this.log("Doing request to server");
      data = [("" + this.imageFieldName + "_name=") + encodeURIComponent(name), ("" + this.imageFieldName + "=") + encodeURIComponent(file)];
      if (meta) {
        data.push(meta);
      }
      return $.ajax({
        url: window.location.pathname,
        data: data.join('&'),
        type: 'POST',
        success: function() {
          return _this.log("File sent to server");
        },
        error: function() {
          return _this.warn("Failed to send file to server");
        }
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
