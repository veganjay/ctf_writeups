#!/bin/sh

pandoc README.md -o README.docx

zip -r HackVent2018_veganjay.zip README.md README.docx images/ solutions/
