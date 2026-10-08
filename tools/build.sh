#!/usr/bin/env bash
# Build outputs/<name>.pdf (Typst) and .docx from outputs/<name>.md.
#   tools/build.sh [name]   default: Helm-Phase-0-Solution-2026-10-09
set -euo pipefail
cd "$(dirname "$0")/../outputs"
name="${1:-Helm-Phase-0-Solution-2026-10-09}"
# Vietnamese editions end in -vi and use figures/vi.
figdir=figures; case "$name" in *-vi) figdir=figures/vi ;; esac

python3 ../tools/diagrams.py            # writes figures/*.svg and figures/vi/*.svg

for svg in figures/*.svg figures/vi/*.svg; do   # PNG copies for the DOCX
  printf '#set page(width: auto, height: auto, margin: 0pt)\n#image("/%s")\n' "$svg" > .fig.typ
  typst compile --root . --ppi 200 .fig.typ "${svg%.svg}.png"
done
rm -f .fig.typ
cp ../tools/conf.typ .conf.typ

pandoc "$name.md" --from markdown --columns=10000 \
  --to typst --standalone -V template=/.conf.typ -M figure-dir="$figdir" \
  --lua-filter=../tools/mermaid-figures.lua --lua-filter=../tools/colwidths.lua \
  -o .build.typ
typst compile --root . .build.typ "$name.pdf"

pandoc "$name.md" --from markdown --columns=10000 -M figure-ext=png -M figure-dir="$figdir" \
  --lua-filter=../tools/mermaid-figures.lua --lua-filter=../tools/colwidths.lua \
  --toc --toc-depth=2 -o "$name.docx"

# .build.typ and .conf.typ are kept (git-ignored) for page previews
echo "Built outputs/$name.pdf and outputs/$name.docx"
