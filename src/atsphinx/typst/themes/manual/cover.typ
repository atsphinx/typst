#let titlepage(body, size: 24pt, vt: 0%) = {
  set align(right)
  set text(size: size, weight: "bold")
  v(vt)
  body
}
#cleanPage(
  [
    #titlepage("{{ document.title }}", size: 24pt, vt: 10%)
    #titlepage("{{ config.release }}", size: 16pt, vt: 0%)
    #titlepage("{{ config.author }}", size: 18pt, vt: 30%)
    #titlepage("{{ date.strftime('%Y-%m-%d') }}", size: 14pt, vt: 40%)
    #pagebreak()
  ]
)
