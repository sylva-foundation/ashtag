module "ashtag"

class ashtag.FileStore
    constructor: () ->
        ashtag.lib.mixins.Logging::augment @

        @imageFieldName = "image"
        @imageMaxWidth = 800
        @imageMaxHeight = 600

        @enabled = @_supported()
        ashtag.lib.mixins.Observable::augment @
        
        # Stop now if the browser doesn't have support
        return if not @enabled
        
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
        if not window.uploaderDb
            window.uploaderDb = window.openDatabase('uploader', '', 'Pending uploads', 5 * 1024 * 1024)
            @log 'Creating and caching database connection'
        return window.uploaderDb

    initialiseDb: ->
        # create the table if necessary
        @db = @getDb()
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

        console?.group?('Storing file')

        return @_readFile(file, meta)
            .then(@_resizeFile)
            .then(@_storeFile)
            .then(@_handleStoreSuccess, @_handleStoreFailure)
            .then(
                -> console.groupEnd()
                -> console.groupEnd()
            )


    _readFile: (file, meta) ->
        # read a file into a FileReader. Returns a promise
        @log "Reading file"
        deferred = $.Deferred()
        reader = new FileReader()
        reader.onloadend = (e) =>
            @log "Reading of #{reader.result.length} bytes complete"
            deferred.resolve(file, reader, meta)
        reader.readAsDataURL(file)
        return deferred.promise()

    _resizeFile: (file, reader, meta) =>
        @log "Resizing file"
        def = $.Deferred()

        canvas = document.createElement "canvas"
        img = new Image()

        handleLoaded = =>
            @log 'Image loaded. Resizing'

            handleRendered = =>
                @log 'Getting image as encoded data'
                resizedData = canvas.toDataURL("image/jpeg")
                @log "Resize complete. Image now #{resizedData.length} bytes"
                
                def.resolve(file, resizedData, meta)

            mpImg = new MegaPixImage(file);
            mpImg.onrender = handleRendered

            parent_this = @ # Slight hack to give us access to both contexts
            EXIF.getData file, ->
                mpImg.render canvas, 
                    orientation: EXIF.getTag(@, 'Orientation')
                    maxWidth: parent_this.imageMaxWidth
                    maxHeight: parent_this.imageMaxHeight

        img.src = reader.result

        @log 'Waiting for image to load'
        interval = setInterval =>
                if img.width > 0
                    clearInterval(interval)
                    handleLoaded()
            , 100

        return def

    _storeFile: (file, fileData, meta) =>
        # store a file into the db. Returns a promise
        @log "Locally storing file with length #{fileData.length}"
        deferred = $.Deferred()
        @query("INSERT INTO [files] ([name], [meta], [file]) VALUES (?, ?, ?)", [file.name, meta, fileData]).then(
            => 
                @log "Storing complete"
                deferred.resolve()
            => 
                @warn "Storing failed"
                deferred.reject()
        )
        return deferred.promise()

    _handleStoreSuccess: =>
        @log "File stored locally successfully"
        # image successfully stored locally, lets 
        # sync if we are online
        return @allToServer()

    _handleStoreFailure: =>
        @warn "Local storage failed"
        # failed to store image locally
    
    allToServer: ->
        # upload all locally stored files to the server. Returns a promise
        @log "Sending all locally stored files to the server"
        deferred = $.Deferred()
        @query("SELECT * FROM [files]").then (rows) =>
            @log "Sending #{rows.length} files"
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
        @log "Popping file to the server"
        deferred = $.Deferred()
        @sendRequest(row.name, row.file, row.meta).then =>
            @log "File sent, deleting from local db"
            @query("DELETE FROM [files] WHERE [id] = ?", [row.id]).then(
                =>
                    @log "Deletion complete"
                    deferred.resolve()
                => 
                    @warn "Deletion failed"
                    deferred.resolve()
            )
        , -> deferred.resolve()
        return deferred.promise()

    sendRequest: (name, file, meta) ->
        # Do the file request to the server
        # For now we assume that 'meta' is url encoded already
        @log "Doing request to server"
        data = [
            "#{@imageFieldName}_name=" + encodeURIComponent(name)
            "#{@imageFieldName}=" + encodeURIComponent(file)
        ]
        if meta
            data.push(meta)

        return $.ajax
            url: window.location.pathname
            data: data.join '&'
            type: 'POST'
            success: => @log "File sent to server"
            error: => @warn "Failed to send file to server"


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


        


