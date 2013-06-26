jQuery ->
    $ = jQuery

    $.ajaxSetup
        cache: false

    # Set the online/offline class
    goOnline = =>
        $('body').addClass('online').removeClass('offline')

    goOffline = =>
        $('body').addClass('offline').removeClass('online')

    window.addEventListener 'online', goOnline
    window.addEventListener 'offline', goOffline
    if ashtag.extra.online
        goOnline()
    else
        goOffline()

    # If there is an appcache update ready
    if window.applicationCache
        applicationCache.addEventListener 'updateready', =>
            $('#updatesready').show();



$(window).on 'pagechange', (event, obj) =>
    # A hack to change the lable on the login form
    if obj.toPage.attr('id') == 'login-page'
        $('.login-page label[for=id_username]').text('Email')

    # Set the action of any forms correctly
    $('form').each (i, el) =>
        $el = $(el)
        if not $el.attr('action')
            $el.attr 'action', $.mobile.activePage.data('url')

