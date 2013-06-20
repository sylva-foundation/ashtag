module "ashtag.panes"

class ashtag.panes.MapBasePane extends ashtag.lib.panes.BasePane

    initialise: ->
        @defaultLat = 54.03
        @defaultLng = -3.67
        @defaultZoom = 5
        @map = null
        @$map = @$('#map_canvas')

    setupEvents: ->

    start: ->
        @setupMap()

    setupMap: ->
        mapOptions =
            center: new google.maps.LatLng(@defaultLat, @defaultLng)
            zoom: @defaultZoom
            mapTypeId: google.maps.MapTypeId.HYBRID

        @map = new google.maps.Map @$map.get(0), mapOptions
        google.maps.event.addDomListener window, 'load', @handleMapLoad

    centerOnUser: ->
        return if not navigator.geolocation

        navigator.geolocation.getCurrentPosition (position) =>
            @setMapLocation(position.coords.latitude, position.coords.longitude)

    handleMapLoad: (e, map) =>
        # Called once map setup is complete

    setMapLocation: (lat, lng) ->
        @map.setCenter new google.maps.LatLng(lat, lng)
        @map.setZoom 8
    