// Cyclone report style for pandoc's Typst writer (`-V template=style/conf.typ`).
// Pandoc calls `conf(...)` with its metadata; unknown arguments are absorbed by `..rest`.

#let ink = rgb("#1b2a41")
#let accent = rgb("#1f6f8b")
#let muted = rgb("#5b6b7f")
#let rule = rgb("#d5dbe3")
#let tint = rgb("#eef3f7")

#let conf(
  title: none,
  subtitle: none,
  authors: (),
  date: none,
  abstract: none,
  lang: "en",
  font: ("Helvetica Neue", "Helvetica", "Arial"),
  fontsize: 10pt,
  codefont: ("Menlo", "DejaVu Sans Mono"),
  linkcolor: none,
  ..rest,
  doc,
) = {
  set document(title: title, date: none)
  set text(font: font, size: fontsize, lang: lang, fill: ink)
  set par(justify: false, leading: 0.62em, spacing: 0.9em)
  show raw: set text(font: codefont, size: 0.9em)

  // Cover page: no header or footer.
  page(paper: "a4", margin: (x: 2.2cm, y: 2.6cm), header: none, footer: none)[
    #v(1fr)
    #text(size: 10pt, fill: accent, weight: "bold", tracking: 0.08em)[PROJECT HELM]
    #v(0.6em)
    #text(size: 26pt, weight: "bold")[#title]
    #if subtitle != none {
      v(0.4em)
      text(size: 14pt, fill: muted)[#subtitle]
    }
    #v(1.6em)
    #line(length: 30%, stroke: 2pt + accent)
    #v(1.2em)
    #for a in authors [
      #text(size: 11pt)[#a.name] \
    ]
    #if date != none [#text(size: 11pt, fill: muted)[#date]]
    #v(2fr)
    #text(size: 8.5pt, fill: muted)[
      #if lang == "vi" [
        Bảo mật. Tài liệu được lập để phục vụ việc ra quyết định nội bộ của Khách hàng.
        Báo cáo này không phải là tư vấn pháp lý, thuế hay đầu tư; các câu hỏi pháp lý
        được nêu để luật sư tư vấn của Khách hàng xem xét.
      ] else [
        Confidential. Prepared for the Client's internal decision-making. This report
        is not legal, tax or investment advice; regulatory questions are identified for
        the Client's legal counsel.
      ]
    ]
  ]

  set page(
    paper: "a4",
    margin: (x: 2.2cm, top: 2.4cm, bottom: 2.2cm),
    header: context {
      set text(size: 8pt, fill: muted)
      [Project Helm · #title]
      h(1fr)
      [Cyclone]
      v(-0.4em)
      line(length: 100%, stroke: 0.5pt + rule)
    },
    footer: context {
      set text(size: 8pt, fill: muted)
      h(1fr)
      counter(page).display("1 / 1", both: true)
    },
  )
  counter(page).update(1)

  set heading(numbering: "1.1")
  // Part headings ("Part I: …") start a page as a small kicker, and the section
  // heading that follows stays on the same page instead of leaving it blank.
  let after-part = state("after-part", false)
  show heading.where(level: 1): it => {
    let is-part = it.numbering == none and (repr(it.body).contains("Part ") or repr(it.body).contains("Phần "))
    context {
      if after-part.get() { after-part.update(false) } else { pagebreak(weak: true) }
    }
    if is-part {
      after-part.update(true)
      block(above: 0pt, below: 0.6em, text(size: 10pt, weight: "bold", fill: accent,
        tracking: 0.06em, upper(it.body)))
    } else {
      set text(size: 18pt, fill: ink)
      block(above: 0pt, below: 1em, it)
    }
  }
  show heading.where(level: 2): set text(size: 13pt, fill: accent)
  show heading.where(level: 3): set text(size: 11pt)
  show heading: set block(above: 1.4em, below: 0.7em)

  show link: set text(fill: accent)
  show outline.entry.where(level: 1): set text(weight: "bold")

  // Tables: compact, tinted header, horizontal rules only.
  set table(
    inset: (x: 5pt, y: 4pt),
    stroke: (_, y) => (
      top: if y <= 1 { 0.7pt + ink } else { 0.4pt + rule },
      bottom: 0.4pt + rule,
    ),
    fill: (_, y) => if y == 0 { tint },
  )
  show table: set text(size: 8.5pt)
  // pandoc wraps tables in align(center); keep cell text left unless a column says otherwise.
  show table: set align(left)
  show table.cell.where(y: 0): set text(weight: "bold")
  show figure.where(kind: table): set block(breakable: true)
  show figure.caption: set text(size: 8.5pt, fill: muted)

  doc
}
