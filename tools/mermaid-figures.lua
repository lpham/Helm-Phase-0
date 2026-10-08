-- Replace ```{.mermaid #fig-name caption="..."} blocks with the pre-rendered
-- SVG outputs/figures/fig-name.svg (PDF) or .png (DOCX). The Markdown source
-- keeps the Mermaid text so it stays editable and renders on GitHub.

local ext = "svg"
local dir = "figures"

function Meta(meta)
  if meta["figure-ext"] then ext = pandoc.utils.stringify(meta["figure-ext"]) end
  if meta["figure-dir"] then dir = pandoc.utils.stringify(meta["figure-dir"]) end
end

function CodeBlock(block)
  if not block.classes:includes("mermaid") then return nil end
  local id = block.identifier
  if id == "" then
    io.stderr:write("mermaid block without #id; left as code\n")
    return nil
  end
  local path = dir .. "/" .. id .. "." .. ext
  local caption = block.attributes["caption"] or ""
  local img = pandoc.Image({}, path, "", { width = "100%" })
  return pandoc.Figure(pandoc.Plain({ img }), { pandoc.Plain(pandoc.Str(caption)) },
    { id = id })
end

return { { Meta = Meta }, { CodeBlock = CodeBlock } }
