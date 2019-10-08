#!/usr/bin/env racket

#lang racket/base


;;; ----------------------------------------------------
;;; Filename: charty.rkt
;;; Author:   Damir Cavar <damir@cavar.me>
;;; Version:  0.2
;;;
;;; (C) 2006-2011 by Damir Cavar
;;;
;;; This code is published under the Lesser GPL!
;;; Please find the text of the LGPL here:
;;; http://www.gnu.org/licenses/lgpl.txt
;;; 
;;; It is free for use, change, etc. as long as the copyright
;;; note above is included in any modified version of the code.
;;;
;;; Usage:
;;;
;;; racket -qtm charty.rkt -g PSG1.txt -s "John kissed Mary"
;;;
;;; or, if charty.rkt is executable
;;;
;;; ./charty.rkt -g PSG1.txt -s "John kissed Mary"
;;;
;;; ----------------------------------------------------


(require srfi/1)
(require racket/file)
(require racket/cmdline)


;-----------------------------------------------------------------------
; some global definitions

(define rule-re (pregexp
                 (string-append
                  "([^-=>#,\\s]+(?:[-]+[^-=>#,\\s]+)*)" ; symbol [^-=>#,\s]+([-]+[^-=>#,\s]+)*
                  "(?:\\s+(?:-+|=+)>\\s+)"              ; arrow or production symbol
                  "([^-=>#,\\s]+(?:[-]+[^-=>#,\\s]+)*(?:\\s+[^-=>#,\\s]+(?:[-]+[^-=>#,\\s]+)*)*)"
                  "(?:\\s+#.*)?"))) ; comment

(struct grammar (lhs lprhs terminals symbols) #:mutable #:transparent)


;-----------------------------------------------------------------------
; the grammar processing functions

(define parse-grammar
  (lambda (grammar-file grammar) ; TODO exception handling for the file->lines procedure
    (for-each
     (lambda (line)
       (let ([lmatch (regexp-match rule-re line)])
         (when (and lmatch
                    (= (length lmatch) 3))
           (let ([lhs (string->symbol (list-ref lmatch 1))]
                 [rhs (map (lambda (token)
                             (string->symbol token))
                           (regexp-split #rx" +" (list-ref lmatch 2)))])
             (hash-set! (grammar-symbols grammar) lhs #t)
             (for-each
              (lambda (token)
                (hash-set! (grammar-terminals grammar) token #t))
              rhs)
             (let ([val  (hash-ref (grammar-lhs grammar)   lhs              '())]
                   [rval (hash-ref (grammar-lprhs grammar) (list-ref rhs 0) '())])
               (unless (member (list lhs rhs) rval)
                 (hash-set! (grammar-lprhs grammar) (list-ref rhs 0) (append rval (list (list lhs (cdr rhs))))))
               (unless (member rhs val)
                 (hash-set! (grammar-lhs grammar) lhs (append val (list rhs)))))))))
     (file->lines grammar-file))
    (for-each
     (lambda (key)
       (hash-remove! (grammar-terminals grammar) key))
     (hash-keys (grammar-symbols grammar)))
    grammar))



(define new-grammar
  (lambda (grammar-file)
    (parse-grammar grammar-file (grammar (make-hash) (make-hash) (make-hash) (make-hash)))))


(define add2grammar
  (lambda (grammar-file ogrammar)
    (parse-grammar grammar-file ogrammar)))


;-----------------------------------------------------------------------
; the parsing functions


(define verbose #f) ; be verbouse, i.e. show chart edges
(define latex   #f)   ; print out latex tree definition


;;; inactive-edge (edge)
;;; true is edge inactive, else false
(define inactive-edge
  (lambda (edge)
    (>= (caddr edge) (length (list-ref edge 4)))))


;;; active-edge (edge)
;;; negation of inactive-edge
(define-syntax-rule (active-edge edge)
  (not (inactive-edge edge)))


(define terminal?
  (lambda (mgrammar token)
    (hash-ref (grammar-terminals mgrammar) token #f)))


(define symbol?
  (lambda (mgrammar token)
    (hash-ref (grammar-symbols mgrammar) token #f)))


;;; rule-invocation
;;; find complete edges and add rules that have the LHS symbol
;;; as the first RHS symbol
(define rule-invocation
  (lambda (mgrammar chart start)
    (let ([res '()])
      (for-each ; edge on chart starting from start
       (lambda (edge)
         (cond [(inactive-edge edge) ; if edge not active
                (let ([rhss (hash-ref (grammar-lprhs mgrammar) (list-ref edge 3) '())])
                  (for-each ; for each RHS with LHS as initial symbol
                   (lambda (x)
                     (let* ([newedge (list (car edge) (cadr edge) 1 (list-ref x 0)
                                           (append (list (list-ref edge 3)) (list-ref x 1))
                                           (append (list (list-index
                                                          (lambda (el)
                                                            (eq? el edge))
                                                          chart))))])
                       (unless (or (member newedge chart)
                                   (member newedge res)); if not on chart or res, append
                         (when verbose
                           (printf "RI new edge: ~a\n" newedge))
                         (set! res (append res (list newedge))))))
                   rhss))]))
       (drop chart start))
      res)))


;;; fundamental-rule
;;; find active edges and axpand them with inactive, i.e.
;;; the first symbol after the dot as their LHS symbol
(define fundamental-rule
  (lambda (chart)
    (let ([res '()])
      (for-each ; edge on chart
       (lambda (edge)
         (cond [(active-edge edge)
                (let ([expectation (list-ref (list-ref edge 4) (caddr edge))])
                  (for-each ; edge on chart
                   (lambda (oe)
                     (cond [(inactive-edge oe)
                            (cond [(and (eq? expectation (list-ref oe 3))
                                        (= (cadr edge) (car oe)))
                                   (let ([newedge (list (car edge) (cadr oe)
                                                        (+ (caddr edge) 1)
                                                        (list-ref edge 3)
                                                        (list-ref edge 4)
                                                        (append (list-ref edge 5)
                                                                (list (list-index
                                                                       (lambda (el)
                                                                         (eq? el oe))
                                                                       chart))))])
                                     (unless (or (member newedge chart)
                                                 (member newedge res))
                                       (when verbose
                                         (printf "FR new edge: ~a\n" newedge))
                                       (set! res (append res (list newedge)))))])]))
                   chart))]))
       chart)
      res)))


(define parse
  (lambda (mgrammar tokens)
    (let ([chart '()])
      (let ([counter 0])
        (for-each
         (lambda (token)
           (let ([vals (hash-ref (grammar-lprhs mgrammar) token '())])
             (for-each (lambda (y) ; create edge with span
                         (let ([edge (list counter (+ counter 1) 1 (list-ref y 0) (append (list token ) (list-ref y 1)) '())])
                           (unless (member edge chart)
                             (when verbose
                               (printf "Init new edge: ~a\n" edge))
                             (set! chart (append chart (list edge))))))
                       vals)
             (set! counter (+ counter 1))))
         tokens))
      (let ([start  0] ; apply rule invocation, fundamental rule, until nothing more possible
            [oldlen (length chart)])
        (let loop ()
          (let ([res (rule-invocation mgrammar chart start)])
            (when (> (length res) 0)
              (set! chart (append chart res))))
          (let ([res (fundamental-rule chart)])
            (when (> (length res) 0)
              (set! chart (append chart res))))
          ; something changed on the chart
          (let ([nlen (length chart)])
            (cond [(> nlen oldlen)
                   (begin
                     (set! oldlen nlen)
                     (loop))]))))
      chart)))


;;; serialize-chart
;;; create lists of complete overspanning edges
(define serialize-chart
  (lambda (mgrammar chart input (with-span #f))
    (let ([end (length input)])
      (for/list ((edge (in-list (reverse chart)))
                 #:when (and (inactive-edge edge) ; inactive edge
                             (= (car edge) 0)     ; from beginning
                             (= (cadr edge) end)))
        (edge->list mgrammar chart edge with-span)))))


;;; edge->list
;;; converts embedded edges into an embedded list
;;; if with-span is #t each node is preceded by its span index
(define edge->list
  (lambda (mgrammar chart edge (with-span #f))
    (let ([analysis (list (list-ref edge 3))])
      (let ([rule-counter 0])
        (for-each
         (lambda (token)
           (if (terminal? mgrammar token)
               (set! analysis (append analysis (list (list-ref (list-ref edge 4) 0))))
               (begin
                 (set! analysis
                       (append analysis
                               (list (edge->list mgrammar chart
                                                 (list-ref chart
                                                           (list-ref (list-ref edge 5) rule-counter)) with-span))))
                 (set! rule-counter (add1 rule-counter)))))
         (list-ref edge 4)))
      analysis)))


;-----------------------------------------------------------------------


(define (sublist l offset n)
  (take (drop l offset) n))


(define main
  (lambda ()
    (let ([grammar-file   ""]
          [input-sentence ""])
      (define sentence-to-parse
        (command-line
         #:program "charty"
         #:once-each
         [("-v" "--verbose") "Verbose mode" (set! verbose #t)]
         [("-l" "--latex") "LaTeX Qtree output mode" (set! latex #t)]
         [("-g" "--grammar") gf "Grammar file name" (set! grammar-file gf)]
         [("-s" "--sentence") is "Input sentence" (set! input-sentence is)]))
      (when (and (> (string-length grammar-file) 0)
                 (> (string-length input-sentence) 0))
        (let ([mygrammar (new-grammar grammar-file)]
              [input (map (lambda (t) (string->symbol t)) (regexp-split #rx" +" input-sentence))])
          (let ([chart (parse mygrammar input)])
            (let ([counter 0])
              (for-each (lambda (x)
                          (set! counter (+ counter 1))
                          (printf "Parse ~a: ~a\n" counter x))
                        (serialize-chart mygrammar chart input #f)))))))))

;(provide main)
(main)
