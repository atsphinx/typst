/*
Render field nodes of reStructuredText.
*/
#let sphinxField(title, content) = {
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
