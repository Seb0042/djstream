#! /bin/bash
set -x
if [ ! -z "$1" ]
then
	SOURCE="$1"
else
	SOURCE="$(cat sourceinfo)"
fi
if [ ! -z "$2" ]
then
	OUTPUT="$2"
else
	OUTPUT="$(cat outputinfo)"
fi
if [ ! -z "$3" ]
then
	TARGET="$3"
else
	TARGET="$(cat targetinfo)"
fi
ffmpeg  $SOURCE $OUTPUT "${TARGET}"
