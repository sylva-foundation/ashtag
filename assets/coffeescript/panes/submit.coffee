module 'ashtag.panes'

class ashtag.panes.SubmitSightingPane extends ashtag.lib.panes.BasePane

    initialise: ->
        # Create the map pane
        @mapPane = new ashtag.panes.SubmitSightingMapPane @$el
        @$form = @$('form')
        @$imageField = @$('form #id_image')
        @$submitButton = @$form.find('.submit-sighting')
        @$offlineMessage = @$form.find('.offline-msg')
        @$savedForLater = @$form.find('.saved-for-later')
        @fileStore = new ashtag.FileStore()
        @updateSavedForLater()

    setupEvents: ->
        @$form.on 'submit', @handleSubmit
        window.addEventListener 'online', @sync

    start: ->
        @sync()

    handleSubmit: (e) =>
        if @online()
            @submitOnline(e)
        else
            @submitOffline(e)

    submitOffline: (e) ->
        e.preventDefault()
        meta = @$form.serialize()
        file = @$imageField.get(0).files[0]
        storePromise = @fileStore.storeFile file, meta

        @showOfflineStorageMessage()

        # Hide the message after storing is complete 
        # and a few seconds have elapsed
        hide = ashtag.extra.callAfter(2, @hideOfflineStorageMessage)
        storePromise.then hide
        setTimeout hide, 4000

    showOfflineStorageMessage: =>
        @$submitButton.parent().hide()
        @$offlineMessage.show()
        @$savedForLater.hide()

    hideOfflineStorageMessage: =>
        @$offlineMessage.hide()
        @$submitButton.parent().show()
        @$savedForLater.show()
        @updateSavedForLater()

    updateSavedForLater: =>
        @fileStore.totalPendingFiles().then (total) =>
            @$savedForLater.find('.total').text total
            @$savedForLater.toggle(!!total)

    submitOnline: (e) ->
        # Don't do anything, just do it the old-fashioned way

    online: ->
        return window.navigator.onLine == true or window.navigator.onLine == undefined

    sync: =>
        console.log('syncing')
        if @online()
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