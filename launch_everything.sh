#!/bin/bash

theme_name=$1
mkdir -p $1/original
mkdir -p $1/deleted
mkdir -p $1/clean

listOfUrls=$2

python generatePageContent.py $2 $1/original
python selectBadFiles.py $1/original $1/deleted
python removeUserParts.py $1/original $1/clean
python dorkCreator.py $1/clean $1_dorks
cp $2 urls/wordpress35/$2
cp $1_dorks dorks/wordpress35/$1_dorks
mv $1_dorks $1/
mv $2 $1/
mv $1 wordpress35/
