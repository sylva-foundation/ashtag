module "ashtag"

class ashtag.FileStore
    constructor: () ->
        @enabled = @_supported()
        ashtag.lib.mixins.Observable::augment @
        
        # Stop now if the browser doesn't have support
        return if not @_supported
        
        @db = @getDb()
        @initialiseDb()
        @pushToServer() # send any pending files

    _supported: ->
        return !!window.openDatabase

    disable: ->
        @enabled = false
        @fire 'disable'

    enable: ->
        @enabled = true
        @fire 'enable'

    getDb: ->
        return window.openDatabase('uploader', '', 'Pending uploads', 10 * 1024 * 1024);

    initialiseDb: ->
        # initialise the db if necessary
        @db.transaction (tx) => 
            tx.executeSql "CREATE TABLE IF NOT EXISTS [files] ( 
                              [id] INTEGER PRIMARY KEY AUTOINCREMENT,
                              [name], [meta], [file]
                          )"
            , []
            , => # success 
                @enable()
            , => # failure; fallback to online uploads
                @disable()

    storeFile: (file, meta='') ->
        # Store the file and meta data, returning a deferred
        if not @enabled
            throw 'Offline uploading disabled'

        @_readFile(file, meta)
            .then(@_storeFile)
            .then(@_handleStoreSuccess, @_handleStoreFailure)


    _readFile: (file, meta) ->
        console.log('read')
        deferred = $.Deferred()
        reader = new FileReader()
        reader.onloadend = (e) =>
            fileData = e.target.result
            deferred.resolve(file.name, fileData, meta)
        reader.readAsDataURL(file)
        return deferred

    _storeFile: (fileName, fileData, meta) =>
        console.log('store')
        deferred = $.Deferred()
        @db.transaction (tx) =>
            tx.executeSql "INSERT INTO [files] ([name], [meta], [file]) VALUES (?, ?, ?)", 
                [fileName, meta, fileData], 
                =>
                    deferred.resolve()
                    # uploader.enable();
                    # uploader.pushQueueToServer();
                =>
                    deferred.reject()
                    # uploader.enable();
        return deferred

    _handleStoreSuccess: =>
        console.log('success')

    _handleStoreFailure: =>
        console.log('failure')
    

    pushToServer: ->
        # upload files to the server