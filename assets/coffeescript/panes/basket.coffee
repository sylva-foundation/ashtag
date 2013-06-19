module "ashtag.panes"

class ashtag.panes.BasketPane extends ashtag.lib.panes.BasePane

    initialise: ->
        @$form = @$('form');
        @$removes = @$('.remove');

    setupEvents: ->
        @$removes.on 'click', (e) =>
            e.preventDefault()
            @remove $(e.target).data('id')

    start: ->


    remove: (id) ->
        $("#id_form-#{id}-DELETE").attr 'checked', 'checked'
        $.mobile.hidePageLoadingMsg()
        @submit().then(@reload)

    submit: ->
        $.post @$form.attr('action'), @$form.serialize()

    reload: =>
        # Reload basket
        $.mobile.changePage window.location.href,
            allowSamePageTransition: true
            transition: 'none'
            reloadPage: true

$(window).on 'pagechange', (event, obj) =>
    if obj.toPage.attr('id') == 'basket-page'
        new ashtag.panes.BasketPane obj.toPage