module "ashtag"

class ashtag.FileStore
    constructor: () ->
        @imageFieldName = "image"
        @imageFieldName = "meta"

        @enabled = @_supported()
        ashtag.lib.mixins.Observable::augment @
        
        # Stop now if the browser doesn't have support
        return if not @_supported
        
        @db = @getDb()
        @initialiseDb()
        @allToServer() # send any pending files

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
                =>
                    deferred.reject()
        return deferred

    _handleStoreSuccess: =>
        console.log('success')

    _handleStoreFailure: =>
        console.log('failure')
    
    allToServer: ->
        # upload files to the server
        deferred = $.Deferred()
        send = =>    
            @popToServer().then ->
                    deferred.notify()
                , ->
                    deferred.resolve()
        deferred.then null, null, send
        send()
        return deferred

    popToServer: ->
        # pop one file off and send it to the server
        deferred = $.Deferred()
        @db.transaction (tx) ->
          tx.executeSql "SELECT * FROM [files] LIMIT 1", [], (tx, res) ->
            if not res.rows.length
                deferred.reject()
            else
                item = res.rows[0]
                console.log(res.rows)
                console.log(item)
                @sendToServer(item.name, item.file, item.meta).then ->
                    tx.executeSql "DELETE FROM [files] WHERE [id] = ?", [item.id],
                        -> deferred.resolve(),
                        -> deferred.resolve()
                , -> deferred.resolve()
        return deferred

    sendToServer: (name, file, meta) ->
        # For now we assume that 'meta' is url encoded already
        data = [
            "#{@imageFieldName}_name=#{name}"
            "#{@imageFieldName}=#{file}"
        ]
        if meta
            data.push(meta)

        return $.ajax
            data: data.join '&'
            type: 'POST'


        


