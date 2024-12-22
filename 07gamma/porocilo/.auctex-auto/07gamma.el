;; -*- lexical-binding: t; -*-

(TeX-add-style-hook
 "07gamma"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("article" "11pt")))
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "path")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "url")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "nolinkurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperbaseurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperimage")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "href")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "path")
   (TeX-run-style-hooks
    "latex2e"
    "../../../preamble"
    "article"
    "art11")
   (LaTeX-add-labels
    "sec:orge7c61fa"
    "sec:orgf12cecc"
    "sec:org322b661"
    "sec:org4af1b3a"
    "sec:orgaba5d65"
    "sec:org6346c70"
    "sec:org8f92a5e"
    "sec:orgb677120"
    "fig:eno"
    "sec:orgb47b656"
    "sec:org39e42a5"
    "fig:sum"
    "sec:org0586687"
    "eq:1"
    "eq:2"
    "sec:org51e535e"
    "sec:org8835c43"
    "sec:orgfb9b95f"
    "sec:orgb8fc457"
    "sec:orgacaf9d4")
   (LaTeX-add-bibliographies
    "refs"))
 :latex)

