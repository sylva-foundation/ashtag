window.module = (name, node=window) ->
	path = []
	
	if typeof name == "string"
		parts = name.split(".")
	else
		parts = name
	
	if parts.length > 1
		node[parts[0]] or= {}
		module(parts[1..parts.length], node[parts[0]])
	else
		node[parts[0]] or= {}

module "ashtag.lib.panes"

class ashtag.lib.panes.BasePane
	requiredParams: []

	constructor: (@$el, @spec={}) ->
		ashtag.lib.mixins.Observable::augment @
		@_requireParams(@requiredParams...) if @requiredParams?.length
		@$el.data 'pane', @
		@initialise()
		@setupEvents()
		@start()
	
	_requireParams: (names...) ->
		for name in names
			if not @spec[name]?
				throw "Param '#{name}' was not specified"
	
	$: (selector) ->
		return jQuery(selector, @$el);

	# Do any initialisation 
	initialise: ->
		
	
	# Setup the event handling
	setupEvents: ->
		
	
	# Everything setup and good to go
	start: ->

