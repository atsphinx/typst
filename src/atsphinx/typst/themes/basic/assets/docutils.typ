/*
Render adomoition
*/
#let admonition(title, content) = {
  pad(
    left: 5%,
    rect(
      width: 90%,
      radius: 1pt,
      [
        #rect(
          title
        )
        #content
      ]
    )
  )
}


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
