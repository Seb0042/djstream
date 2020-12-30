#! /bin/bash
set -x
if [ ! -z "$1" ]
then
	TARGET="$1"
else
	TARGET="$(cat djinfo)"
fi
ffmpeg -ac 2 -f alsa -i hw:1,0 -acodec libmp3lame -ab 32k -ac 2 -content_type audio/mpeg -f mp3 "${TARGET}"
