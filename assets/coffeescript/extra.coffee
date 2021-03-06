module "ashtag.extra"

ashtag.extra.track = (o) ->
	if window._gat
		for tracker in window._gat._getTrackers()
			tracker._trackEvent(o.category, o.action, o.label, o.value, o.nonInteraction)
	else if window._gaq
		window._gaq.push ['_trackEvent', o.category, o.action, o.label, o.value, o.nonInteraction]

# This is a simple utility for running a callback after a certain number of
# tries. This can be useful when a callback needs to be run once operations
# within a loop have been completed, and were those operations only return
# following a callback.
#
# Example:
#
#     var fn = ashtag.extra.callAfter(myList.length, theCallback).go;
#     for(i in myList) {
#         doSomethingWithCallbackOnCompletion(fn)
#     }

ashtag.extra.callAfter = (count, callback) ->
    callCount = 0

    return (args...) ->
        callCount += 1
        if callCount == count
            callback args...

ashtag.extra.online = ->
    return window.navigator.onLine == true or window.navigator.onLine == undefined

ashtag.extra.whenOnline = ->
    def = $.Deferred()
    $(window).on 'online', =>
        def.resolve()
    if ashtag.extra.online
        def.resolve()
    return def

ashtag.extra._locationPromise = null
ashtag.extra.geoLocate = =>
    # Geolocate the user and return a promise. 
    # The result is cached.
    def = $.Deferred()
    if not navigator.geolocation
        def.reject()
        return def.promise()

    if ashtag.extra._locationPromise
        return ashtag.extra._locationPromise

    navigator.geolocation.getCurrentPosition(
        (position) =>
            def.resolve(position.coords.latitude, position.coords.longitude)
        (error) =>
            def.reject()
        timeout: 20000
    )

    ashtag.extra._locationPromise = def
    return def.promise()

ashtag.extra.isLatLngSane = (lat, lng) ->
    # Bounds around the UK
    bounds = 
        lat:
            max: 63 
            min: 48
        lng:
            max: 3
            min: -12

    if lat > bounds.lat.max or lat < bounds.lat.min
        return false
    if lng > bounds.lng.max or lat < bounds.lng.min
        return false
    return true

ashtag.extra.getQueryParameter = (name) ->
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    regex = new RegExp("[\\?&]#{name}=([^&#]*)")
    results = regex.exec(location.search);
    return if results == null then "" else decodeURIComponent(results[1].replace(/\+/g, " "))
