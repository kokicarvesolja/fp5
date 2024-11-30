;; -*- lexical-binding: t; -*-

(TeX-add-style-hook
 "05nmr"
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
    "sec:orgf006394"
    "eq:1"
    "eq:2"
    "eq:3"
    "eq:4"
    "eq:6"
    "eq:5"
    "sec:org02fc6c0"
    "sec:org4d45467"
    "sec:org93542d4"
    "sec:org135c7a5"
    "fig:prosta_procesija"
    "fig:spinski_odmev"
    "fig:t2_zvezdica"
    "sec:orgd2f454d"
    "fig:umeritev"
    "sec:org45f3957"
    "fig:t1_ion"
    "fig:t1_tap"
    "sec:orgefcfe41"
    "fig:spinski_t2"
    "sec:org50e2e3d")
   (LaTeX-add-bibliographies
    "refs"))
 :latex)

