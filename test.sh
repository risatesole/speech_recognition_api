#!/bin/bash
curl -X 'POST' \
  'http://127.0.0.1:8000/transcribe' \
  -H 'accept: application/json' \
  -F 'audio=@./audio.wav'
