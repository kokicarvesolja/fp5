;; -*- lexical-binding: t; -*-

(TeX-add-style-hook
 "08gammagamma"
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
    "sec:org254d4af"
    "sec:org9bc5234"
    "sec:orge32db56"
    "sec:org032569d"
    "fig:caspot"
    "fig:prisig"
    "sec:org81fd923"
    "fig:casloc"
    "sec:orgb5a1d2e"
    "eq:1"
    "fig:radraz"
    "eq:2"
    "fig:logradraz"
    "sec:orgbb3588f"
    "fig:koivrh"
    "eq:3"
    "fig:test"
    "sec:org1a6bddf"))
 :latex)

