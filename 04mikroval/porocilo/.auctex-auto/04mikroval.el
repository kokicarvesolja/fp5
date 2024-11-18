;; -*- lexical-binding: t; -*-

(TeX-add-style-hook
 "04mikroval"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("article" "11pt")))
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "href")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperimage")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperbaseurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "nolinkurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "url")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "path")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "path")
   (TeX-run-style-hooks
    "latex2e"
    "../../../preamble"
    "article"
    "art11")
   (LaTeX-add-labels
    "sec:org9f570f6"
    "fig:1"
    "eq:1"
    "eq:2"
    "eq:3"
    "eq:4"
    "sec:org0f556ee"
    "sec:orgc5da1f2"
    "sec:orgb6430b5"
    "sec:orgb9f4d6a"
    "fig:umeritev"
    "sec:org4464617"
    "fig:zajem_signala"
    "fig:krivulja_ubranosti"
    "fig:x_min"
    "eq:5"
    "tab:rodovi")
   (LaTeX-add-bibliographies
    "refs"))
 :latex)

