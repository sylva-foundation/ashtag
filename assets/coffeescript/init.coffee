window._gaq = window._gaq or []

jQuery ->
    $ = jQuery

    $.ajaxSetup
        cache: false

    # Set the online/offline class
    goOnline = =>
        $('body').addClass('online').removeClass('offline')

    goOffline = =>
        $('body').addClass('offline').removeClass('online')

    $(window).on 'online', goOnline
    $(window).on 'offline', goOffline
    if ashtag.extra.online
        goOnline()
    else
        goOffline()

    # If there is an appcache update ready
    if window.applicationCache
        applicationCache.addEventListener 'updateready', =>
            $('#updatesready').show();

    # Are we logged in?
    $.ajax
        url: '/session-status/'
        type: 'get'
        dataType: 'json'
    .then (data) ->
        $('body')
            .toggleClass('authenticated', data.authenticated)
            .toggleClass('anonymous', not data.authenticated)
            .toggleClass('ios', data.phonegap)
            .toggleClass('non-ios', not data.phonegap)



$(window).on 'pagechange', (event, obj) =>
    currentUrl = $.mobile.activePage.data('url')

    # A hack to change the lable on the login form
    if obj.toPage.attr('id') == 'login-page'
        $('.login-page label[for=id_username]').text('Email')

    # Set the action of any forms correctly
    $('form').each (i, el) =>
        $el = $(el)
        if not $el.attr('action')
            $el.attr 'action', currentUrl

    # Google analytics page view tracking
    window._gaq.push(['_trackPageview', currentUrl])
