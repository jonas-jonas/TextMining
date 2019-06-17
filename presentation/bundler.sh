#!/bin/bash

hash inotifywait 2>/dev/null || { echo >&2 "inotifywait is required to run this script. Please install it using sudo apt-get install inotify-tools."; exit 1; }

if [ ! -d "output" ]; then
    mkdir output
fi

if [ ! -d "output/reveal.js" ]; then 
    git clone -b 3.7.0 --depth 1 https://github.com/hakimel/reveal.js.git output/reveal.js
fi

bundle exec asciidoctor-revealjs \
    -D output/ \
    -a revealjsdir=reveal.js src/index.adoc \
    --trace

xdg-open "http://localhost:3000" &

trap 'kill $!' SIGINT
python3 -m http.server -d output 3000 > /dev/null 2>&1 &
inotifywait -m ./src -e close_write |
while read path action file; do
    if [[ "$file" =~ .*adoc$ ]]; then 
        bundle exec asciidoctor-revealjs \
            -D output/ \
            -a revealjsdir=reveal.js src/index.adoc \
            --trace
        echo "Built Output"
    fi
done
