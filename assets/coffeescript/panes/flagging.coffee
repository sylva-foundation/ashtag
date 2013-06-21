module "ashtag.panes"

class ashtag.panes.FlaggingPane extends ashtag.lib.panes.BasePane
    # handles flagging button interactions

    initialise: ->
        @$flagButtons = @$('.report-button')
        @$sendReportButton = @$('#send-report')
        @$dialogFlagType = @$('.dialog-flag-type')

    setupEvents: ->
        @$flagButtons.unbind().bind 'click', @handleFlagClick
        @$sendReportButton.unbind().bind 'click', @handleReportClick

    start: ->

    handleFlagClick: (event) =>
        $el = $(event.currentTarget)
        @flag_type = $el.attr('data-flag-type')
        @flag_id = $el.attr('data-flag-id')
        @handled_button = $el
        @$dialogFlagType.html " #{@flag_type}"

    handleReportClick: (event) =>
        args = {}
        args[@flag_type] = @flag_id
        switch @flag_type
            when 'tree'
                url = "/sightings/tree/#{@flag_id}/flag/"
            when 'sighting'
                url = "#{location.pathname}flag/"
        $.post url,
            args,
            @handleResponse

    handleResponse: (data, textStatus, jqXHR) =>
        switch @flag_type
            when 'sighting'
                if 'remove' of data.sighting
                    $("#sighting-#{data.sighting.remove}").fadeOut()
                else
                    @handled_button.hide()
                    @handled_button.hide().after('<div class="reported">Reported.</div>')
            when 'tree'
                @handled_button.hide().after('<div class="reported">Reported.</div>')

$(window).on 'pagechange', (event, obj) =>
    new ashtag.panes.FlaggingPane obj.toPage


