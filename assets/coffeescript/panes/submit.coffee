module 'ashtag.panes'

class ashtag.panes.SubmitSightingPane extends ashtag.lib.panes.BasePane

    initialise: ->
        # Create the map pane
        @$form = @$('form')
        @$imageField = @$('form #id_image')
        @$submitButton = @$form.find('.submit-sighting')
        @$submitDoneMessages = @$form.find('.submit-done-msgs')
        @$savedForLater = @$form.find('.saved-for-later')
        @$locationInput = @$form.find('#id_location')

        @mapPane = new ashtag.panes.SubmitSightingMapPane @$el, @parseLocation()
        @fileStore = new ashtag.FileStore()
        @updateSavedForLater()

    setupEvents: ->
        @$form.on 'submit', @handleSubmit
        window.addEventListener 'online', @sync
        @mapPane.observe 'locationChange', (e, lat, lng) => @updateLocation(lat, lng)

    updateLocation: (lat, lng) =>
        @$locationInput.val "POINT (#{lng} #{lat})"

    start: ->
        @sync()

        return ashtag.extra.geoLocate().then @updateLocation, =>
            # Failed. If we are offline then show the user an error
            # (as we cannot show them the map if they are offline)
            if not ashtag.extra.online()
                alert 'Could not get your location. Find an Internet connection and try again'

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

    parseLocation: ->
        # Parse the lat/lng out of the location input
        text = @$locationInput.val()
        return if not text
        re = /^POINT\s*\(([-\.\d]+) ([-\.\d]+)\)$/g
        match = re.exec(text)
        return {} =
            lat: parseFloat(match[2], 10)
            lng: parseFloat(match[1], 10)


$(window).on 'pagechange', (event, obj) =>
    if obj.toPage.attr('id') == 'submit-sighting-page'
        new ashtag.panes.SubmitSightingPane obj.toPage