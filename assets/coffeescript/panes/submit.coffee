module "ashtag.panes"

class ashtag.panes.SubmitSightingPane extends ashtag.lib.panes.BasePane

    initialise: ->
        # Create the map pane
        @mapPane = new ashtag.panes.SubmitSightingMapPane @$el
        @$form = @$('form')
        @$imageField = @$('form #id_image')
        @fileStore = new ashtag.FileStore()


    setupEvents: ->
        @$form.on 'submit', @handleSubmit

    start: ->

    handleSubmit: (e) =>
        e.preventDefault()
        meta = @$form.serialize()
        file = @$imageField.get(0).files[0]
        @fileStore.storeFile file, meta




$(window).on 'pagechange', (event, obj) =>
    if obj.toPage.attr('id') == 'submit-sighting-page'
        new ashtag.panes.SubmitSightingPane obj.toPage