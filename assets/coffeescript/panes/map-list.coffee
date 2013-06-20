module "ashtag.panes"

class ashtag.panes.MapListPane extends ashtag.panes.MapBasePane

    handleMapLoad: (e, map) =>
        super
        @centerOnUser()
        @getLocations().then(@renderLocations)

    getLocations: ->
        # The the tree locations and return a deferred
        $.getJSON "/api/v1/tree/"

    renderLocations: (json) =>
        # render the locations onto the map
        for tree in json.objects
            @addTree(tree)

    handleMarkerClick: (event, marker) ->
        if marker.tree.tag_number
            # Only for tagged trees
            $.mobile.changePage marker.tree.view_url

    addTree: (tree) ->
        latLng = new google.maps.LatLng tree.latlng[0], tree.latlng[1]

        if tree.tag_number
            icon =
                url: 'https://maps.google.com/mapfiles/kml/shapes/parks.png'
                scaledSize:
                    width: 24
                    height: 24
        else
            icon = 
                url: 'https://maps.google.com/mapfiles/kml/paddle/red-circle-lv.png'
                scaledSize:
                    width: 24
                    height: 24

        markerOpts = 
            icon: icon
            position: latLng
            map: @map

        marker = new google.maps.Marker markerOpts
        marker.tree = tree
        google.maps.event.addListener marker, 'click', (e) => @handleMarkerClick(e, marker)


$(window).on 'pagechange', (event, obj) =>
    if obj.toPage.attr('id') == 'map-page'
        new ashtag.panes.MapListPane obj.toPage