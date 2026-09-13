.PHONY: test test-starter perf list
test:            ## run every reference solution's test-suite
	python3 -m pytest problems -q
test-starter:    ## run YOUR starter.py for one problem:  make test-starter Q=q01
	IMPL=starter python3 -m pytest problems/$(Q)* -q
perf:            ## only the perf tests
	python3 -m pytest problems -q -m perf
list:
	python3 drill.py list
