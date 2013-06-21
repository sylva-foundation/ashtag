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
        @setupMap()

    setupMap: ->
        mapOptions =
            center: new google.maps.LatLng(@defaultLat, @defaultLng)
            zoom: @defaultZoom
            mapTypeId: google.maps.MapTypeId.HYBRID
        @map = new google.maps.Map @$map.get(0), mapOptions
        google.maps.event.addListenerOnce @map, 'idle', @handleMapLoad

    centerOnUser: ->
        deferred = $.Deferred()
        if not navigator.geolocation
            deferred.resolve(@defaultLat, @defaultLng)
        else
            navigator.geolocation.getCurrentPosition(
                (position) =>
                    deferred.resolve(position.coords.latitude, position.coords.longitude)
                (error) =>
                    deferred.resolve(@defaultLat, @defaultLng)
                timeout: 10000
            )

        # Center the map once we have a location
        deferred.then (lat, lng) =>
            @setMapLocation lat, lng, @zoomedInZoomLevel

        return deferred.promise()

    handleMapLoad: (e, map) =>
        # Called once map setup is complete

    setMapLocation: (lat, lng, zoom) ->
        @map.setCenter new google.maps.LatLng(lat, lng)
        @map.setZoom zoom
    
