#!/bin/bash

cd /home && celery -A tasks worker --loglevel=info
