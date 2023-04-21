(require 'org)
(require 'ox)

(setq org-export-with-toc nil)
(setq org-export-with-smart-quotes t)

(add-to-list 'org-export-smart-quotes-alist '("en_GB"
     (primary-opening :utf-8 "‘" :html "&lsquo;" :latex "`" :texinfo "`")
     (primary-closing :utf-8 "’" :html "&rsquo;" :latex "'" :texinfo "'")
     (secondary-opening :utf-8 "“" :html "&ldquo;" :latex "``" :texinfo "``")
     (secondary-closing :utf-8 "”" :html "&rdquo;" :latex "''" :texinfo "''")
     (apostrophe :utf-8 "’" :html "&rsquo;")))

(setq org-latex-classes
      '(("memoir" "\\documentclass[11pt,oneside]{memoir}\n[NO-DEFAULT-PACKAGES]\n[EXTRA]"
         ("\\chapter{%s}" . "\\chapter*{%s}")
         ("\\section{%s}" . "\\section*{%s}")
         ("\\subsection{%s}" . "\\subsection*{%s}")
         ("\\subsubsection{%s}" . "\\subsubsection*{%s}")
         ("\\paragraph{%s}" . "\\paragraph*{%s}")
         ("\\subparagraph{%s}" . "\\subparagraph*{%s}"))))
