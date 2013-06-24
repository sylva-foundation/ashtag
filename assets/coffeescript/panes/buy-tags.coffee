module "ashtag.panes"

class ashtag.panes.BuyTagsPane extends ashtag.lib.panes.BasePane

    initialise: ->
        @includeShippingInPrice = false

        @$tagPackInput = @$('.select-tags select, input#product_id[type=hidden]')
        @$quantityInput = @$('.quantity select')
        @$price = @$('.price-placehodler')
        @$postagePrice = @$('.postage-price')

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
        return parseFloat(@$postagePrice.text(), 10)

    getPackPrice: ->
        packPrice = @$tagPackInput.data('price') or @$tagPackInput.find('option:selected').data('price')
        return parseFloat(packPrice, 10)

    getQuantity: ->
        quantity = @$quantityInput.find('option:selected').val() or 1
        return parseInt(quantity, 10)


$(window).on 'pagechange', (event, obj) =>
    if obj.toPage.attr('id') == 'buy-tags-page'
        new ashtag.panes.BuyTagsPane obj.toPage