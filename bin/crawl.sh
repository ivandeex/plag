#!/bin/bash
extra_args="$*"
set -x
scrapy crawl -L WARN $extra_args hidemyass
