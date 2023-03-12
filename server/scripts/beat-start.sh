#! /usr/bin/env bash
set -e
celery -A celery_app.app beat -l info
