module "ashtag.panes"

class ashtag.panes.MapListPane extends ashtag.panes.MapBasePane

    handleMapLoad: (e, map) =>
        super
        @getLocations().then(@renderLocations)

    getLocations: ->
        # The the tree locations and return a deferred
        $.getJSON "/api/v1/marker/",
            limit: 0

    renderLocations: (json) =>
        # render the locations onto the map
        for tree in json.objects
            @addTree(tree)

    handleMarkerClick: (event, marker) ->
        $.mobile.changePage marker.tree.view_url

    _getMarkerIcon: (tree) ->
        tagged = if tree.tag_number then 'tagged' else 'untagged'
        if tree.disease_state == true
            probability = 'likely'
        else if tree.disease_state == false
            probability = 'unlikely'
        else if tree.disease_state == null
            probability = 'uncertain'

        return "/static/images/markers/#{tagged}-#{probability}.png"

    addTree: (tree) ->
        latLng = new google.maps.LatLng tree.latlng[0], tree.latlng[1]

        if tree.tag_number
            icon =
                url: @_getMarkerIcon(tree)
                scaledSize:
                    width: 32
                    height: 32
        else
            icon = 
                url: @_getMarkerIcon(tree)
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
