module "ashtag.extra"

ashtag.extra.track = (o) ->
	if window._gat
		for tracker in window._gat._getTrackers()
			tracker._trackEvent(o.category, o.action, o.label, o.value, o.nonInteraction)
	else if window._gaq
		window._gaq.push ['_trackEvent', o.category, o.action, o.label, o.value, o.nonInteraction]
