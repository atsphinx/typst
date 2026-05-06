{% include '!basic/layout.typ' %}

#let contentPage(body) = context {
  let headerText = "{{ config.project }} {{ config.release }}"
  let pos(cur, total) = {
    if calc.odd(total - cur) and calc.odd(cur) {
      return left
    }
    if calc.odd(total - cur) and calc.even(cur) {
      return right
    }
    if calc.even(total - cur) and calc.odd(cur) {
      return right
    }
    if calc.even(total - cur) and calc.even(cur) {
      return left
    }
  }
  page(
    numbering: "1",
    header: context {
      let totalPageNum = here().page();
      let currentPageNum = counter(page).get().first();

      align(pos(currentPageNum, totalPageNum))[#headerText]
      line(length: 100%, stroke: 2pt + black);
    },
    footer: context {
      let totalPageNum = here().page();
      let currentPageNum = counter(page).get().first();

      line(length: 100%, stroke: 1pt + black);
      align(pos(currentPageNum, totalPageNum))[#currentPageNum]
    },
    [
      #body
    ]
  )
}

#set heading(numbering: "1.1.")
#show heading.where(level: 1): it => {
  let count = counter(heading).at(here()).first()
  if count > 1 {
    pagebreak()
  }
  [
    #align(right)[#it]
    #v(18pt)
  ]
}
#show heading.where(level: 2): it => [
  #v(36pt)
  #it
  #v(18pt)
]
#show heading.where(level: 3): it => [
  #v(24pt)
  #it
  #v(12pt)
]

#show raw.where(block: true): it => {
  rect(
    width: 100%,
    fill: rgb("#f8f8f8"),
    stroke: (paint: rgb("#4a5568"), thickness: 1pt),
    radius: 0pt,
    inset: 16pt,
    {
      it
    }
  )
}

#show raw.where(block: false): it => {
  box(
    fill: rgb("#cccccc").lighten(80%),
    radius: 0pt,
    outset: 1pt,
    it
  )
}

#show figure.where(kind: raw): it => {
  set align(start)
  block(width: auto, breakable: false)[
    #show figure.caption: set align(center)
    #it
  ]
}
