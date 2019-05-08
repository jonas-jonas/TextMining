#!/bin/bash

hash inotifywait 2>/dev/null || { echo >&2 "inotifywait is required to run this script. Please install it using sudo apt-get install inotify-tools."; exit 1; }

PWD=$(pwd)

if [[ $PWD =~ .*\/text_mining$ ]]; then
    PWD="${PWD}/submission"
fi

THEME="article"
STYLES_DIR="${PWD}/themes"
FONTS_DIR="${PWD}/themes/fonts"
ENTRY_FILE="${PWD}/article.adoc"
DESTINATION_DIR="${PWD}/../generated" # Hack to reach the generated folder in project root

if [ "$1" == "--watch" ]; then
    # Watch for changes in adoc files and regenerate the pdf
    inotifywait -m $PWD -e close_write |
    while read path action file; do
        if [[ "$file" =~ .*adoc$ ]]; then 
            asciidoctor-pdf -a pdf-stylesdir=$STYLES_DIR -a pdf-style=$THEME -a pdf-fontsdir=$FONTS_DIR $ENTRY_FILE -D $DESTINATION_DIR
        fi
    done
else
    #Publish
    asciidoctor-pdf -a pdf-stylesdir=$STYLES_DIR -a pdf-style=$THEME -a pdf-fontsdir=$FONTS_DIR $ENTRY_FILE -D $DESTINATION_DIR
    echo "Generated article.pdf in 'generated' directory."
fi

