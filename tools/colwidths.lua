-- Give wide tables column widths proportional to how much text each column holds.
-- Without this, pandoc emits auto widths and Typst can squeeze a prose-heavy
-- column into a narrow strip (for example the weekly plan in section 8).

local function cell_text(cell)
  return pandoc.utils.stringify(cell.contents)
end

local function longest_word(text)
  local best = 0
  for word in text:gmatch("%S+") do
    best = math.max(best, utf8.len(word) or #word)
  end
  return best
end

function Table(tbl)
  local ncols = #tbl.colspecs
  if ncols < 3 then return nil end

  local total, word, rows = {}, {}, 0
  for i = 1, ncols do total[i] = 0; word[i] = 0 end
  local function add(row)
    for i, cell in ipairs(row.cells) do
      if i <= ncols then
        local text = cell_text(cell)
        total[i] = total[i] + (utf8.len(text) or #text)
        word[i] = math.max(word[i], longest_word(text))
      end
    end
  end
  for _, row in ipairs(tbl.head.rows) do add(row) end
  for _, body in ipairs(tbl.bodies) do
    for _, row in ipairs(body.body) do add(row); rows = rows + 1 end
  end
  if rows == 0 then return nil end

  -- Damp the differences so short columns stay readable, but never make a
  -- column narrower than its longest word (plus room for cell padding).
  local weights, sum = {}, 0
  for i = 1, ncols do
    weights[i] = math.max((total[i] / rows) ^ 0.75, word[i]) + 2
    sum = sum + weights[i]
  end
  for i = 1, ncols do
    tbl.colspecs[i] = { tbl.colspecs[i][1], weights[i] / sum }
  end
  return tbl
end
