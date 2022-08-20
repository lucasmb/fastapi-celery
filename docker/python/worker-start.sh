#!/bin/bash

set -o errexit
set -o nounset

celery -A app.main.celery worker --loglevel=info
