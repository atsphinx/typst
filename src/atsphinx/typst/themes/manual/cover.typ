#let titlepage(body, size: 24pt, vt: 0%) = {
  set align(right)
  set text(size: size, weight: "bold")
  v(vt)
  body
}

#cleanPage(
  [
    #titlepage([{{ title }}], size: 24pt, vt: 10%)
    #titlepage([{{ release }}], size: 16pt, vt: 0%)
    #titlepage([{{ author }}], size: 18pt, vt: 30%)
    #titlepage([{{ date }}], size: 14pt, vt: 40%)
    #pagebreak()
  ]
)
