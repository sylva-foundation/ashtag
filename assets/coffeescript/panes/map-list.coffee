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
                url: '/static/images/map-tree-icon-green.png'
                scaledSize:
                    width: 32
                    height: 32
        else
            icon = 
                url: '/static/images/map-tree-icon-orange.png'
                scaledSize:
                    width: 18
                    height: 18

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
