#!/bin/sh
PROXY="10.243.251.11:3128"
export http_proxy="http://$PROXY"
export https_proxy="https://$PROXY"
export HTTP_PROXY="http://$PROXY"
export HTTPS_PROXY="https://$PROXY"
export no_proxy="127.0.0.1,localhost,10.243.251.70"
export NO_PROXY="$no_proxy"

python ./chatbot.py
