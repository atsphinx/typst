/*
* Render <desc> node in Sphinx.
*
* Refs: https://www.sphinx-doc.org/en/master/extdev/nodes.html#sphinx.addnodes.desc
*/
#let desc(
  signature,
  content,
) = {
  pad(5%)[
    #signature
    #pad(left: 5%)[
      #block()[
        #content
      ]
    ]
  ]
}
