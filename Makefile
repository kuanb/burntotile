.PHONY: build clean deploy serve

DIST := dist

## Build a self-contained dist/index.html (MapLibre JS + CSS inlined)
build: $(DIST)/index.html

$(DIST)/index.html: index.html build.py
	@mkdir -p $(DIST)
	python3 build.py index.html $(DIST)/index.html

## Remove build artefacts
clean:
	rm -rf $(DIST)

## Push dist/index.html to the gh-pages branch (force, orphan history)
deploy: build
	@echo "Deploying $(DIST)/index.html → gh-pages branch..."
	@set -e; \
	  REMOTE=$$(git remote get-url origin); \
	  TMP=$$(mktemp -d); \
	  cp $(DIST)/index.html $$TMP/; \
	  cd $$TMP && git init && git checkout -b gh-pages && \
	  git add index.html && \
	  git commit -m "deploy $$(date -u +%Y-%m-%dT%H:%M:%SZ)"; \
	  git push -f $$REMOTE HEAD:gh-pages; \
	  rm -rf $$TMP
	@echo "Done. Set GitHub Pages source to the gh-pages branch if not already."

## Serve the built file locally
serve: build
	python3 -m http.server 8000 --directory $(DIST)
