; lexc-mode-el -- Major mode for editing LEXC files

; Author: W.P. McNeill <billmcn@u.washington.edu>
; Created: 7 November 2004
; Keywords: LEXC major-mode

; This program is free software; you can redistribute it and/or
; modify it under the terms of the GNU General Public License as
; published by the Free Software Foundation; either version 2 of
; the License, or (at your option) any later version.

; This program is distributed in the hope that it will be
; useful, but WITHOUT ANY WARRANTY; without even the implied
; warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
; PURPOSE.  See the GNU General Public License for more details.

; You should have received a copy of the GNU General Public
; License along with this program; if not, write to the Free
; Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
; MA 02111-1307 USA

; This was based on an emacs mode authoring tutorial located here:
; http://two-wugs.net/emacs/mode-tutorial.html



; Hook for overriding the functions defined in this file
(defvar lexc-mode-hook nil)

; Associate .lexc extension with this mode.
(add-to-list 'auto-mode-alist '("\\.lexc\\'" . lexc-mode))

; Keywords for syntax highlighting
(defconst lexc-font-lock-keywords
  (list
   '("\\<\\(Multichar_Symbols\\)\\>" . font-lock-keyword-face)
   '("\\<\\(LEXICON\\)\\>" . font-lock-function-name-face))
  "Highlighting expressions for LEXC mode.")

; Define syntactic constituents
(defvar lexc-mode-syntax-table
  (let ((lexc-mode-syntax-table (make-syntax-table)))
    ; The ! character is the comment delimiter
    (modify-syntax-entry ?!  "<" lexc-mode-syntax-table)
    (modify-syntax-entry ?\n ">" lexc-mode-syntax-table)
    lexc-mode-syntax-table)
  "Syntax table for lexc-mode")

; Entry function called by emacs  
(defun lexc-mode ()
  (interactive)
  (kill-all-local-variables)
  ; Define syntactic constituents
  (set-syntax-table lexc-mode-syntax-table)
  ; Set up font-lock
  (set (make-local-variable 'font-lock-defaults) '(lexc-font-lock-keywords))
  ; Register our indentation function
  (setq major-mode 'lexc-mode)
  (setq mode-name "LEXC")
  (run-hooks 'lexc-mode-hook))

; Expose this mode to the emacs environment
(provide 'lexc-mode)




