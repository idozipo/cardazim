#!/bin/bash
set -x

python -m cardazim.client 127.0.0.1 5000 "my_card" "Ido" "What is the time?" "15:00" "image.png"