#!/bin/sh
echo '<?xml version="1.0" encoding="UTF-8"?>'
echo '<patches>'
for f in $*; do
  n=${f//httpd-2\.[0-9]\.[0-9][0-9]-/}
  n=${n//.patch/}
  s_HEAD=`grep ^Upstream-HEAD $f | sed 's/Upstream-HEAD: //'`
  s_20=`grep ^Upstream-2.0: $f | sed 's/Upstream-2.0: //'`
  s_Com=`grep ^Upstream-Status: $f | sed 's/Upstream-Status: //'`
  s_PR=`grep ^Upstream-PR: $f | sed 's/Upstream-PR: //'`
  printf ' <patch name="%s">\n' $n
  printf '  <status branch="HEAD">%s</status>\n' "$s_HEAD"
  printf '  <status branch="2.0">%s</status>\n' "$s_20"
  printf '  <comment>%s</comment>\n' "$s_Com"
  if [ -n "$s_PR" ]; then
    printf '  <bug pr="%s"/>\n' "$s_PR"
  fi
  printf ' </patch>\n'
done
echo '</patches>'
