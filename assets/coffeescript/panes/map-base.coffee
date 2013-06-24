module "ashtag.panes"

class ashtag.panes.MapBasePane extends ashtag.lib.panes.BasePane

    initialise: ->
        @defaultLat = 54.03
        @defaultLng = -3.67
        @defaultZoom = 5
        @zoomedInZoomLevel = 8
        @map = null
        @$map = @$('#map_canvas')

    setupEvents: ->

    start: ->
        ashtag.extra.whenOnline().then =>
            @setupMap()

    setupMap: ->
        mapOptions =
            center: new google.maps.LatLng(@defaultLat, @defaultLng)
            zoom: @defaultZoom
            mapTypeId: google.maps.MapTypeId.HYBRID
        @map = new google.maps.Map @$map.get(0), mapOptions
        google.maps.event.addListenerOnce @map, 'idle', @handleMapLoad

    centerOnUser: ->
        promise = ashtag.extra.geoLocate()
        promise.then(
            # Success, got a location
            (lat, lng) => @setMapLocation lat, lng, @zoomedInZoomLevel
            # Failed, used default location
            => @setMapLocation @defaultLat, @defaultLat, @defaultZoom
        )
        return promise

    handleMapLoad: (e, map) =>
        # Called once map setup is complete

    setMapLocation: (lat, lng, zoom) ->
        @map.setCenter new google.maps.LatLng(lat, lng)
        @map.setZoom zoom

