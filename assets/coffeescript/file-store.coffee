module "ashtag"

class ashtag.FileStore
    constructor: () ->
        @imageFieldName = "image"

        @enabled = @_supported()
        ashtag.lib.mixins.Observable::augment @
        
        # Stop now if the browser doesn't have support
        return if not @_supported
        
        @db = @getDb()
        @initialiseDb()

    _supported: ->
        return !!window.openDatabase

    disable: ->
        # Disable offline uploading through the FileStore
        @enabled = false
        @fire 'disable'

    enable: ->
        # Disable offline uploading through the FileStore
        @enabled = true
        @fire 'enable'

    getDb: ->
        # Get the db connection
        return window.openDatabase('uploader', '', 'Pending uploads', 10 * 1024 * 1024)

    initialiseDb: ->
        # create the table if necessary
        @query("CREATE TABLE IF NOT EXISTS [files] ( 
                    [id] INTEGER PRIMARY KEY AUTOINCREMENT,
                    [name], [meta], [file]
                )")
        .then(
            => @enable() #success
            => @disable() # failure; fallback to online uploads
        )

    storeFile: (file, meta='') ->
        # Store the file and meta data, returning a promise
        if not @enabled
            throw 'Offline uploading disabled'

        @_readFile(file, meta)
            .then(@_storeFile)
            .then(@_handleStoreSuccess, @_handleStoreFailure)


    _readFile: (file, meta) ->
        # read a file into a FileReader. Returns a promise
        deferred = $.Deferred()
        reader = new FileReader()
        reader.onloadend = (e) =>
            fileData = e.target.result
            deferred.resolve(file.name, fileData, meta)
        reader.readAsDataURL(file)
        return deferred.promise()

    _storeFile: (fileName, fileData, meta) =>
        # store a file into the db. Returns a promise
        deferred = $.Deferred()
        @query("INSERT INTO [files] ([name], [meta], [file]) VALUES (?, ?, ?)", [fileName, meta, fileData]).then(
            -> deferred.resolve()
            -> deferred.reject()
        )
        return deferred.promise()

    _handleStoreSuccess: =>
        # image successfully stored locally

    _handleStoreFailure: =>
        # failed to store image locally
    
    allToServer: ->
        # upload all locally stored files to the server. Returns a promise
        deferred = $.Deferred()
        @query("SELECT * FROM [files]").then (rows) =>
            send = =>
                row = rows.pop()
                if row
                    @popToServer(row).then ->
                        deferred.notify()
                else
                    deferred.resolve()

            deferred.then null, null, send
            send()

        return deferred.promise()

    popToServer: (row) ->
        # send the file specified by the db row `row` to the server. Returns a promise
        deferred = $.Deferred()
        @sendRequest(row.name, row.file, row.meta).then =>
            @query("DELETE FROM [files] WHERE [id] = ?", [row.id]).then(
                -> deferred.resolve()
                -> deferred.resolve()
            )
        , -> deferred.resolve()
        return deferred.promise()

    sendRequest: (name, file, meta) ->
        # Do the file request to the server
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

    query: (sql, values=[]) ->
        # Utility method to run queries against the server. Returns a promise
        deferred = $.Deferred()
        @db.transaction (tx) =>
            tx.executeSql sql, values, (tx, res) =>
                rows = []
                while rows.length < res.rows.length
                    rows.push res.rows.item(rows.length)
                deferred.resolve rows
        return deferred.promise()

    totalPendingFiles: ->
        deferred = $.Deferred()
        @query('SELECT COUNT(*) AS count FROM [files]').then (rows) ->
            deferred.resolve rows[0].count
        return deferred.promise()


        


