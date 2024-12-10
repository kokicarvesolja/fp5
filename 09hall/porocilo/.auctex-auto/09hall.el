;; -*- lexical-binding: t; -*-

(TeX-add-style-hook
 "09hall"
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
    "sec:org4245ae2"
    "sec:orgfbbc1a9"
    "eq:1"
    "eq:2"
    "sec:org1c9d802"
    "sec:orgb97d12e"
    "sec:org054ebb6"
    "sec:org46b2437"
    "sec:org6fdafc2"
    "sec:orgb67dd5c"
    "sec:org1e5d2b3"
    "sec:org895ea45"
    "sec:org24f504a"))
 :latex)

