#!/bin/bash

feed:
	python feed.py

update:
	git add .
	git commit
	git push -u origin master