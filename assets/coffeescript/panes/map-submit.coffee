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

    parseLocation: ->
        text = @$locationInput.val()
        return if not text
        re = /^POINT\s*\(([-\.\d]+) ([-\.\d]+)\)$/g
        match = re.exec(text)
        return {} =
            lat: parseFloat(match[2], 10)
            lng: parseFloat(match[1], 10)

    createMarker: ->
        marker = new google.maps.Marker
            position: new google.maps.LatLng(@defaultLat, @defaultLng)
            draggable: true
            bounds: false
            map: @map

        google.maps.event.addDomListener marker, 'dragend', @handleDragEnd

    handleDragEnd: (e) =>
        @updateLocation e.latLng.lat(), e.latLng.lng()

    updateLocation: (lat, lng) ->
        @$locationInput.val "POINT (#{lng} #{lat})"

    handleMapLoad: =>
        super
        @createMarker()



$(window).on 'pagechange', (event, obj) =>
    if obj.toPage.attr('id') == 'submit-sighting-page'
        new ashtag.panes.SubmitSightingMapPane obj.toPage