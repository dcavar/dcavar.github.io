;	$Id: xfst-mode.el,v 1.9 2005/04/13 14:37:24 jens Exp $	
; xfst-mode-el -- Major mode for editing XFST files

; Author: W.P. McNeill <billmcn@u.washington.edu>
; Created: 7 November 2004
; Keywords: XFST major-mode

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

;----------------------------------------------------------
; Modified by Jens Pönninghaus 
; 2005-04-08
; Changed regex construction and added highlighting for some frequently used keywords
; Added highlighting for char sequence definitions using xfst's {}
; Added highlighting for .o. and .x. operators
; Enabled show-paren-mode by default 
; Modified syntax-table
; Added lisp-style indentation 
;        This will most likely produce funny indents *sometimes* 
;        due to lisp-keyword/punctuation detection and prefix vs. infix mismatch 
;        However it is better than having no identation at all

;2005-04-11
; Added a local-keymap
; Added quick'n dirty hack to run current file against xfst
; Added (un-) comment-region 
; Added regex-parser for compile 
;       This works only approximately for multi-line 'input' 
;       but at least it takes you close to the troublespot (usually of-by-one line)
;
;2005-04-12 
; Added insert-define-template to insert an empty define []; string
; Added 'find-matching-definition'  to find definition for symbol under point, if any
; Added run-interactive - to run xfst interactively 
;2005-04-13 changed run-interactive 


;-------------------------------------------------------------------------------------

(require 'compile)
(require 'thingatpt) ; provides word-at-point




; Hook for overriding the functions defined in this file
(defvar xfst-mode-hook nil)

; Associate .xfst extension with this mode.
(add-to-list 'auto-mode-alist '("\\.xfst\\'" . xfst-mode))

; Keywords for syntax highlighting
(defconst xfst-font-lock-keywords
  (let ((kw1 (mapconcat 'identity ; join keywords using regexp or (inefficient but easy :-) change this to regexp-opt
	'(
	  "clear stack"
	  "define"
	  "undefine"
	  "list"
	  "load defined"
	  "load stack"
	  "pop stack"
	  
	  "push defined"
	  "read lexc"
	  "read prolog"
	  "read regex"
	  "read spaced-text"
	  
	  "read text"
	  "rotate stack"
	  "save defined"
	  "save stack"
	  "turn stack"
	  "stack"
	  "undefine"
	  "push"
	  "unlist"
	  "write prolog"
	  "write spaced-text"
	  "write text"
	  "apply up" 
	  "apply down"
	  "print upper"
	  "print lower")
	"\\|")))
    (list
     
     (list (concat "\\<\\(" kw1 "\\)\\>") ; 
	   0 'font-lock-keyword-face)
     '("\\(\\.\\(o\\|x\\)\\.\\)" . 1) ; operators
     '("{\\([^\\{}]+?\\)}"  1 font-lock-string-face) ; highlight character sequence definitions  as 'strings'
     ))
  "Highlighting expressions for XFST mode.")
  

;---------

(defvar xfst-mode-map ()
  "Keymap used in `xfst-mode' buffers.")

(setq xfst-mode-map (make-sparse-keymap))
;; electric keys
(define-key xfst-mode-map "\C-c\C-c" 'xfst-run-current-script )
(define-key xfst-mode-map "\C-c\C-i" 'xfst-interactive-run)
(define-key xfst-mode-map "\C-c#" 'xfst-comment-region )
(define-key xfst-mode-map "\C-c'" 'xfst-uncomment-region )
(define-key xfst-mode-map "\C-c\C-d" 'xfst-insert-define-template )
(define-key xfst-mode-map "\C-c\C-f" 'xfst-find-matching-definition)


;-------

(defvar xfst-block-comment-prefix  "##" "*Blockquote for xfst") ; user-changable definition


(defun xfst-comment-region (beg end &optional arg)
  "Like `comment-region' but uses double hash (`xfst-block-comment-prefix') comment starter."
  (interactive "r\nP")
  (let ((comment-start xfst-block-comment-prefix))
    (comment-region beg end arg)))

(defun xfst-uncomment-region (beg end &optional arg)
  "Like `uncomment-region' but uses double hash (`xfst-block-comment-prefix') comment starter."
  (interactive "r\nP")
  (let ((comment-start xfst-block-comment-prefix))
    (uncomment-region beg end arg)))


(setq compilation-error-regexp-alist
      (cons (list "\\*\\*\\* Error on line \\([0-9]+\\) in file [']\\(.+\\)['][.]" 2 1) ; Error-msg from xfst
	    compilation-error-regexp-alist))
					; provides a regex to parse xfst's error messages


(defun xfst-insert-define-template () "insert an empty definition"
  (interactive)
  (progn 
    (beginning-of-line 2)
    (insert "define ")
    (set-mark (point))
    (insert "  [ ];\n")
    (exchange-point-and-mark)
    ))

(defun xfst-find-matching-definition () "find definition to symbol under point"
  (interactive)
  (xfst-find-definition (word-at-point))
  )


(defun xfst-find-definition (string) "find the define line for a 'symbol'"
  (set-mark (point))
  (if
      (search-backward-regexp (concat "^\\s-*define\\Sw+" string  "\\Sw") ;whitespace* define wsp xfst-symbol non-word-character 
			      nil ;no limit 
			      1 ;no error
			      )
      (prin1 "defined")
    (progn 
      (if 
	  (search-forward-regexp (concat "^\\s-*define\\Sw+" string  "\\Sw") ;whitespace* define wsp xfst-symbol non-word-character 
			     nil ;no limit 
			     1 ;no error
			     )
	  
	  (prin1 "defined right here or even later 'Watch for recursive defs'")
	(prin1 "no active definition found"))
      (exchange-point-and-mark) 
      
      )
    ))
;---------



; Define syntactic constituents
(defvar xfst-mode-syntax-table
  (let ((xfst-mode-syntax-table (make-syntax-table)))
    ; The ! character is the comment delimiter
    ;     # as well
    (modify-syntax-entry ?!  "<" xfst-mode-syntax-table)
    (modify-syntax-entry ?#  "<" xfst-mode-syntax-table) ; support for #-comments
    (modify-syntax-entry ?\n ">" xfst-mode-syntax-table)
    (modify-syntax-entry ?%  "\\" xfst-mode-syntax-table); escape
    (modify-syntax-entry ?\[ "(]" xfst-mode-syntax-table);paren
    (modify-syntax-entry ?\] ")[" xfst-mode-syntax-table);paren
    (modify-syntax-entry ?\| "." xfst-mode-syntax-table); or is puntiuation
    (modify-syntax-entry ?\_ "." xfst-mode-syntax-table); 'here' is punct
    (modify-syntax-entry ?\$ "." xfst-mode-syntax-table); '$' is punct


    xfst-mode-syntax-table)
  "Syntax table for xfst-mode")

(defun xfst-interactive-run ()
  "start local xfst processor"
  (interactive)
  (let ((file (buffer-file-name (current-buffer)))
	(cmd (concat xfst-command " " xfst-command-args " ")))
    (progn
      (save-some-buffers nil nil)
      (shell-command  (concat cmd file " &") ); start asyncronous 
					
      )))


(defun xfst-run-current-script ()
  "start local xfst processor"
  (interactive)
  (let ((file (buffer-file-name (current-buffer)))
	(cmd (concat xfst-command " " xfst-command-batch-args " ")))
    (progn
      (save-some-buffers nil nil)
      (compile-internal (concat cmd file) "No more errors")
					;(shell-command (concat cmd file))
      )))


; Entry function called by emacs  
(defun xfst-mode ()
  (interactive)
  (kill-all-local-variables)
  ; Define syntactic constituents
  (set-syntax-table xfst-mode-syntax-table)

  (use-local-map xfst-mode-map)
  ; Set up font-lock
  (set (make-local-variable 'font-lock-defaults) '(xfst-font-lock-keywords))
  ; Register our indentation function
  (setq 
	major-mode 'xfst-mode
	indent-line-function 'lisp-indent-line ; borrow indentation from lisp-mode
	comment-start "#"
	)
  (setq mode-name "XFST")
  (show-paren-mode 1); enable paren-highlighting
  (run-hooks 'xfst-mode-hook))


(defcustom xfst-command "c:/Programme/xfst/xfst" 
 "Shell command to start fst " 
 :type 'string
  :group 'xfst
)

(defcustom xfst-command-args "-l"
  "string of arguments to be used when starting a fst shell."
  :type 'string
  :group 'xfst)

(defcustom xfst-command-batch-args "-f"
  "string of arguments to be used when starting a fst shell."
  :type 'string
  :group 'xfst)






; Expose this mode to the emacs environment
(provide 'xfst-mode)
