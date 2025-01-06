;; -*- lexical-binding: t; -*-

(TeX-add-style-hook
 "10esr"
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
    "sec:org2f7b62e"
    "sec:org7199d4b"
    "sec:org6464457"
    "sec:org74240be"
    "sec:org1f22431"
    "eq:1"
    "fig:gfaktor"
    "sec:org17b2783"))
 :latex)

