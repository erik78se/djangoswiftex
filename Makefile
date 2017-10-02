.PHONY: test
test:
	@tox

build:
	@charm build -rl DEBUG

push:
	@charm push `echo $(JUJU_REPOSITORY)`/builds/django-worker cs:~jamesbeedy/django-worker
