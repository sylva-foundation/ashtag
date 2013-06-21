module "ashtag.panes"

class ashtag.panes.SubmitSightingMapPane extends ashtag.panes.MapBasePane

    initialise: ->
        super
        @$locationInput = $('#id_location')
        loc = @parseLocation()
        if loc
            @defaultLat = loc.lat
            @defaultLng = loc.lng
            @defaultZoom = 19
        else
            @doLocateUser = true
            @zoomedInZoomLevel = 19

    parseLocation: ->
        text = @$locationInput.val()
        return if not text
        re = /^POINT\s*\(([-\.\d]+) ([-\.\d]+)\)$/g
        match = re.exec(text)
        return {} =
            lat: parseFloat(match[2], 10)
            lng: parseFloat(match[1], 10)

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
        @updateLocation(lat, lng)

    handleDragEnd: (e) =>
        @updateLocation e.latLng.lat(), e.latLng.lng()

    handleMapClick: (e) =>
        @createMarker(e.latLng.lat(), e.latLng.lng())
        @updateLocation e.latLng.lat(), e.latLng.lng()

    updateLocation: (lat, lng) ->
        @$locationInput.val "POINT (#{lng} #{lat})"

    handleMapLoad: =>
        super
        google.maps.event.addDomListener @map, 'click', @handleMapClick
        if @doLocateUser
            @centerOnUser().then(@createMarker)
        else
            @createMarker(@defaultLat, @defaultLng)
