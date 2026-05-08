#let cleanPage(body) = {
  page(
    header: none,
    footer: none,
    [
      #body
    ]
  )
}

#let contentPage(body) = context {
  page(
    numbering: "1 / 1",
    header: none,
    [
      #body
    ]
  )
}
