module 'ashtag.panes'

class ashtag.panes.SubmitSightingPane extends ashtag.lib.panes.BasePane

    initialise: ->
        # Create the map pane
        @mapPane = new ashtag.panes.SubmitSightingMapPane @$el
        @$form = @$('form')
        @$imageField = @$('form #id_image')
        @$submitButton = @$form.find('.submit-sighting')
        @$submitDoneMessages = @$form.find('.submit-done-msgs')
        @$savedForLater = @$form.find('.saved-for-later')
        @fileStore = new ashtag.FileStore()
        @updateSavedForLater()

    setupEvents: ->
        @$form.on 'submit', @handleSubmit
        window.addEventListener 'online', @sync

    start: ->
        @sync()

    handleSubmit: (e) =>
        # Use the filestore if it is available, even if 
        # we are online (the process is more robust and 
        # will resize images)
        if @fileStore.enabled
            @submitViaFileStore(e)
        else
            @submitTraditional(e)

    submitViaFileStore: (e) ->
        # Do the form submission using the FileStore
        e.preventDefault()
        meta = @$form.serialize()
        file = @$imageField.get(0).files[0]
        storePromise = @fileStore.storeFile file, meta

        @showOfflineStorageMessage()

        # Hide the message after storing is complete 
        # and a few seconds have elapsed
        hide = ashtag.extra.callAfter(2, @hideOfflineStorageMessage)
        setTimeout hide, 4000
        storePromise.then hide, =>
            # Failed, so disable the filestore and try the old-school way
            @fileStore.disable()
            @$form.submit()

    submitTraditional: (e) ->
        # Don't do anything, just do it the old-fashioned way

    showOfflineStorageMessage: =>
        @$submitButton.parent().hide()
        @$submitDoneMessages.show()
        @$savedForLater.hide()

    hideOfflineStorageMessage: =>
        @$submitDoneMessages.hide()
        @$submitButton.parent().show()
        @$savedForLater.show()
        @updateSavedForLater()

    updateSavedForLater: =>
        @fileStore.totalPendingFiles().then (total) =>
            @$savedForLater.find('.total').text total
            @$savedForLater.toggle(!!total)

    sync: =>
        if ashtag.extra.online()
            @fileStore.totalPendingFiles().then (total) =>
                if total
                    @handleSyncStart()
                    @fileStore.allToServer().then @handleSyncEnd, @handleSyncEnd, @handleSyncProgress

    handleSyncStart: =>
        return if @syncing # already syncing
        @syncing = true
        $.mobile.loading 'show',
            text: ''
            textVisible: true
        @handleSyncProgress() # update the syncing text

    handleSyncEnd: =>
        @syncing = false
        $.mobile.loading 'hide'
        @updateSavedForLater()

    handleSyncProgress: =>
        @updateSavedForLater()
        @fileStore.totalPendingFiles().then (total) =>
            $('.ui-loader h1').text "Syncing sightings, #{total} remaining"


$(window).on 'pagechange', (event, obj) =>
    if obj.toPage.attr('id') == 'submit-sighting-page'
        new ashtag.panes.SubmitSightingPane obj.toPage