#!/bin/bash

# builds zip file for Ankiweb

latestTag=$(git describe --match "addon21.v*")
retVal=$?
if [ ! $retVal -eq 0 ]; then
    echo "Error, exiting without building"
    exit $retVal
fi
outFile="anki-template-editor-$latestTag.zip"
git archive --format zip --output "$outFile" "$latestTag":addon21

