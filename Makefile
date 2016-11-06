.PHONY: ui

ui:
	sh -c "cd ui && npm install && ng build"
	cp ui/dist/*.js unsorted/static
