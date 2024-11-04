#!/usr/bin/bash
set -euf -o pipefail

. /opt/build123d/bin/activate
inotifywait -e close_write -m . |
while read -r directory events filename; do
	if [[ "$filename" = *.py ]]; then
		python "$directory$filename" || true
	fi
done
