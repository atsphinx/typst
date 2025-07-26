/*
Render field nodes of reStructuredText.
*/
#let field(title, content) = {
  block(
    {
      title
      linebreak()
      pad(
        left: 2em,
        content,
      )
    }
  )
}
