module "ashtag.panes"

class ashtag.panes.BuyTagsPane extends ashtag.lib.panes.BasePane

    setupEvents: ->
        console.log 'BuyTagsPane'

    start: ->


if $('#buy-tags-page').length
    new ashtag.panes.BuyTagsPane $('#buy-tags-page')