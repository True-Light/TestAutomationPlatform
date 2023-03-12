#! /usr/bin/env bash
set -e
celery -A celery_app.app worker -l info -Q interface-test,celery -c 2
