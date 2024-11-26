;; -*- lexical-binding: t; -*-

(TeX-add-style-hook
 "06xrays"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("article" "11pt")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("svg" "")))
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
    "art11"
    "svg")
   (LaTeX-add-labels
    "sec:org9821085"
    "sec:org77d27ca"
    "sec:org639605f"
    "eq:1"
    "sec:org794e03d"
    "eq:2"
    "sec:orgbbc0edf"
    "sec:org2919fcb"
    "sec:orge92d4a4"
    "sec:orgffcac4c"
    "sec:orgdf50172"
    "sec:org5aad74f"
    "fig:nasicenost"
    "tab:ekspo"
    "sec:orgfe9b6b1"
    "sec:org9f235ad"
    "sec:orgf7768b9")
   (LaTeX-add-bibliographies
    "refs"))
 :latex)

