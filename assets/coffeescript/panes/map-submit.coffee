module "ashtag.panes"

class ashtag.panes.SubmitSightingMapPane extends ashtag.panes.MapBasePane

    initialise: ->
        super
        if @spec.lat and @spec.lng
            @defaultLat = @spec.lat
            @defaultLng = @spec.lng
            @defaultZoom = 19
        else
            @doLocateUser = true
            @zoomedInZoomLevel = 19

    createMarker: (lat, lng) =>
        if not @marker
            @marker = new google.maps.Marker
                position: new google.maps.LatLng(lat, lng)
                draggable: true
                bounds: false
                map: @map
        else
            @marker.setPosition(new google.maps.LatLng(lat, lng))

        google.maps.event.addDomListener @marker, 'dragend', @handleDragEnd
        @locationChange(lat, lng)

    handleDragEnd: (e) =>
        @locationChange e.latLng.lat(), e.latLng.lng()

    handleMapClick: (e) =>
        @createMarker(e.latLng.lat(), e.latLng.lng())
        @locationChange e.latLng.lat(), e.latLng.lng()

    locationChange: (lat, lng) ->
        @fire 'locationChange', lat, lng

    handleMapLoad: =>
        super
        google.maps.event.addDomListener @map, 'click', @handleMapClick
        if @doLocateUser
            @centerOnUser().then(@createMarker)
        else
            @createMarker(@defaultLat, @defaultLng)
