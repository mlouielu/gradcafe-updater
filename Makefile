update-results:
	poetry run python run.py > results

check:
	$(eval REMOVE_LINE := $(shell git diff --numstat results| cut -d '	' -f 2))
	$(shell [ $(REMOVE_LINE) -gt 0 ] && git checkout results)

update: check
	git add -u .
	git commit -m 'Update'


.PHONY: check
