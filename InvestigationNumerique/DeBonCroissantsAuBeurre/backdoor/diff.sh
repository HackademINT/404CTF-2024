#!/bin/sh

## Ensures a single file has changed between the official and backdoored package.
## This is meant to avoid heavy reverse-engineering of the entire package when playing the challenge.

set -e

if [ "$#" -ne 2 ]
then
	echo "Usage: $0 official_package backdoor_package"
	exit 1
fi


temp_dir="/tmp/$(date +%s%N)"
mkdir -p "$temp_dir/official"
mkdir -p "$temp_dir/backdoor"


cp "$1" "$temp_dir/official.tar.zst"
cp "$2" "$temp_dir/backdoor.tar.zst"

pushd "$temp_dir"
echo "Working in temporary directory: $(pwd)"

tar xpvf "official.tar.zst" --xattrs-include='*.*' --numeric-owner -C official
tar xpvf "backdoor.tar.zst" --xattrs-include='*.*' --numeric-owner -C backdoor

echo "Extracted packages successfully."

echo "Removing metadata files"
rm */.*

echo "Diffing..."
diff -r official backdoor > diff || true
echo "Diffing done."
cat diff

diff_count="$(cat diff | wc -l)"
echo "Found $diff_count different files (we want 1)"

test "$diff_count" -eq 1
