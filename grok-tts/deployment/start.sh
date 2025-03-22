#!/bin/bash
service nginx start
gunicorn --config gunicorn_config.py app:app
