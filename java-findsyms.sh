#!/bin/zsh

mydir=$(dirname $0)
if [ "$1" = "-v" ]; then
	inverse=1
	shift
else
	inverse=0
fi
string=$1
dir=$2

check() {
	f=$1
	haveSym=0
	$mydir/java-dumpsyms.py $f 2>/dev/null | { while read l; do
		[ "$l" = "$string" ] && haveSym=1 && break
	done; }
	[ $inverse = 0 ] && [ $haveSym = 1 ] && echo $f
	[ $inverse = 1 ] && [ $haveSym = 0 ] && echo $f
}

if [ "$dir" != "" ]; then
	for f in $dir/**/*.java; do
		check $f
	done
else
	while read f; do
		check $f
	done
fi
