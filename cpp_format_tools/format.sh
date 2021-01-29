#!/bin/bash

set -e

FIND="find /otel -name third_party -prune -o -name tools -prune -o -name .git -prune -o -name _deps -prune -o -name .build -prune -o -name out -prune -o -name .vs -prune -o"

echo "Running sed: "
echo "-> Correct common miscapitalizations."
sed -i 's/Open[t]elemetry/OpenTelemetry/g' $($FIND -type f -print)
echo "-> No CRLF line endings, except Windows files."
sed -i 's/\r$//' $($FIND -name '*.ps1' -prune -o \
  -name '*.cmd' -prune -o -type f -print)
echo "-> No trailing spaces."
sed -i 's/ \+$//' $($FIND -type f -print)

echo "Running clang-format $(clang-format --version 2>&1)."
clang-format -i -style=file $($FIND -name '*.cc' -print -o -name '*.h' -print)

echo "Running cmake-format $(cmake-format --version 2>&1)."
cmake-format -i $($FIND -name 'CMakeLists.txt' -print -name '*.cmake' -print -name '*.cmake.in' -print)

echo "Running buildifier"
buildifier $($FIND -name WORKSPACE -print -o -name BUILD -print -o \
    -name '*.BUILD' -o -name '*.bzl' -print)
