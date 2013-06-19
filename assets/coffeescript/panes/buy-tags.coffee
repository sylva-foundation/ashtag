module "ashtag.panes"

class ashtag.panes.BuyTagsPane extends ashtag.lib.panes.BasePane

    initialise: ->
        @includeShippingInPrice = true

        @$tagPackInput = @$('.select-tags select')
        @$quantityInput = @$('.quantity select')
        @$price = @$('.price-placehodler')

    setupEvents: ->
        @$tagPackInput.on 'change', @updatePrice
        @$quantityInput.on 'change', @updatePrice

    start: ->
        @updatePrice()

    updatePrice: =>
        formattedPrice = Number(@getPrice()).toFixed(2)
        @$price.text(formattedPrice)

    getPrice: ->
        price = @getPackPrice() * @getQuantity()
        if @includeShippingInPrice
            price += @getShipping()
        return price

    getShipping: ->
        return 3 # Revisit this later when shipping prices change

    getPackPrice: ->
        packPrice = @$tagPackInput.find('option:selected').data('price')
        return parseInt(packPrice, 10)

    getQuantity: ->
        quantity = @$quantityInput.find('option:selected').val()
        return parseInt(quantity, 10)


$ ->
    if $('#buy-tags-page').length
        new ashtag.panes.BuyTagsPane $('#buy-tags-page form')