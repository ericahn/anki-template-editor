#!/bin/bash

# builds zip file for Ankiweb

echo "Finding latest Anki 2.0 addon release"
latestTag=$(git describe --match "addon20.v*" --abbrev=0)
retVal=$?
if [ ! $retVal -eq 0 ]; then
    echo "Error, exiting without building"
    exit $retVal
fi
outFile="builds/anki-template-editor-$latestTag.zip"
echo "Found, building $outFile"
git archive --format zip --output "$outFile" "$latestTag":addon20

