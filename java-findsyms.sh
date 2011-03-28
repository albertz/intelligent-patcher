#!/bin/zsh

mydir=$(dirname $0)

for f in $2/**/*.java; do
	haveSym=0
	$mydir/java-dumpsyms.py $f 2>/dev/null | { while read l; do
		[ "$l" = "$1" ] && haveSym=1 && break
	done; }
	[ $haveSym = 1 ] && echo $f
done

