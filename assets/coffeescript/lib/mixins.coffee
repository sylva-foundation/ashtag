module "ashtag.lib.mixins"

class ashtag.lib.mixins.Mixin
    # author: https://gist.github.com/993415
    
    # "Class method". Augment object or class `t` with new methods.
    augment: (t) ->
        (t[n] = m unless n == 'augment' or n == 'eject' or n == 'setupMixin' or n == 'constructor' or !this[n].prototype?) for n, m of this
        @setupMixin.call(t)

    # When an object is augmented with at least one mixin, call this method to
    # remove `mixin`.
    eject: (mixin) ->
        (delete this[n] if m in (p for o, p of mixin::)) for n, m of this

    # Implement in your mixin to act as a constructor for mixed-in properties
    setupMixin: ->
        
    

class ashtag.lib.mixins.Observable extends ashtag.lib.mixins.Mixin
    
    @eventNamesMatch: (eventMasks, eventName) ->
        if typeof eventMasks != "object"
            eventMasks = [eventMasks]
        
        for eventMask in eventMasks
            if eventMask == eventName
                return eventMask
            
            if eventMask == "*"
                return eventMask
            
            # Match "foo." to "foo.bar"
            isOpenEnded = (eventMask[eventMask.length - 1] == ".")
            if isOpenEnded and eventName.substr(0, eventMask.length) == eventMask
                return eventMask
            
            # Match ".bar" to "foo.bar"
            isOpenFronted = (eventMask[0] == ".")
            if isOpenFronted and eventName.substr(-eventMask.length) == eventMask
                return eventMask
        
        return false
    
    setupMixin: () ->
        @registry = []
    
    observe: (name, fn) ->
        for item in @registry
            if item.name == name && item.fn == fn
                return false
        @registry.push(name: name, fn: fn)
        return true
    
    unobserve: (name, fn) ->
        @registry.splice(k, 1) for v, k in @registry when item.name == name and item.fn == fn
    
    unobserveAll: ->
        for v, k in @registry
            delete @registry[k].name
            delete @registry[k].fn
        @registry = []
    
    unobserveAllBy: (eventMask) ->
        for v, k in @registry
            if ashtag.Observable.eventNamesMatch(eventMask, v.name)
                @registry.splice(k, 1) # remove from registry
                k -= 1
    
    observeOnce: (name, fn) ->
        wrapper: (params...) ->
            @unobserve(name, wrapper)
            return fn.apply(this, params)
        @observe(name, wrapper)
    
    ###
    Fire an event which can be observed by observe()
    
    name - The name of the event
    data - An array of values that will be passed to the observing function as individual parameters
    scope - The scope in which the observing function will be called
    ###
    fire: (name, params...) ->
        # We collect & execute the functions in two loops, as 
        # the functions may side-effect the registry via a call
        # to unobserve()
        fns = []
        names = []
        for v in @registry
            matchedBy = ashtag.lib.mixins.Observable.eventNamesMatch(name, v.name)
            if matchedBy
                fns.push(v.fn)
                names.push(v.name)
        
        for fn, k in fns
            params.unshift # add the event object to the front of the list
                originalName: name
                eventName: name
                observingFor: names
                matchedBy: matchedBy
                data: params.slice(0) # Clone the params
            
            fn.apply(@, params)
        
    

