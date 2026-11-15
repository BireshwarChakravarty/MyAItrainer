#!/usr/bin/env bash
# Builds the course from src/ into:
#   dist/course.html  - body-only page (for Claude Artifact publishing)
#   index.html        - full standalone HTML document (open locally or host on GitHub Pages)
set -euo pipefail
cd "$(dirname "$0")"
PARTS=(src/00-head.html src/01-shell.html src/m01.html src/m02.html src/m03.html src/m04.html src/m05.html src/m06.html src/m07.html src/m08.html src/m09.html src/m10.html src/m11.html src/m12.html src/90-extras.html src/99-script.html)
mkdir -p dist
cat "${PARTS[@]}" > dist/course.html
{
  echo '<!doctype html>'
  echo '<html lang="en">'
  echo '<head>'
  echo '<meta charset="utf-8">'
  echo '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
  cat src/00-head.html
  echo '</head>'
  echo '<body>'
  cat "${PARTS[@]:1}"
  echo '</body>'
  echo '</html>'
} > index.html
echo "Built dist/course.html ($(wc -c < dist/course.html) bytes) and index.html ($(wc -c < index.html) bytes)"
