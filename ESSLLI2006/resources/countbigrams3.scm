":"; exec mzscheme -r $0 "$@"

;;; ----------------------------------------------------
;;; Filename: countbigrams3.scm
;;; Author:   Damir Cavar <dcavar@me.com>
;;;
;;; (C) 2006 by Damir Cavar
;;;
;;; This code is published under the restrictive GPL!
;;; Please find the text of the GPL here:
;;; http://www.gnu.org/licenses/gpl.txt
;;; 
;;; It is free for use, change, etc. as long as the copyright
;;; note above is included in any modified version of the code.
;;; 
;;; This script assumes that the text is raw and encoded in UTF8.
;;;
;;; Functions:
;;; 1. The text file is loaded into memory.
;;; 2. The text is tokenized, i.e. converted into a list of tokens.
;;; 3. Two adjacent tokens are placed into a hash-table as keys, the value
;;;    is the absolute frequency (i.e. count) of each token in the
;;;    text.
;;; 4. The hash-table is converted into a list of key-value tuples.
;;; 5. The key-values are sorted by value, and a list of bigrams
;;;    and their frequency is printed out.
;;;
;;; If the command line parameters contain more than one text file,
;;; the above results are accumulated over all the input text files.
;;;
;;; Usage:
;;; mzscheme -r countbigrams3.scm test1.txt test2.txt ...
;;; ----------------------------------------------------


;;; all necessary libraries and functions
(require (lib "list.ss"))
(require (lib "string.ss"))   ; for string-uppercase!
(require (lib "string.ss"     "srfi" "13"))
(require (lib "vector-lib.ss" "srfi" "43"))  ; for vector-for-each
(require (lib "pregexp.ss"))  ; for Perl compatible regular expressions

(load "english.scm")

;;; Global variables
(define bigramcount 0.0)                      ; total number of bigrams
(define bigrams     (make-hash-table 'equal)) ; hash-table container for bigram-count pairs


;;; sort-by-value
;;; <- hash-table
;;; -> list of key-value tuples (lists)
;;; ----------------------------------------------------
;;; Sort a hash-table of key-value pairs by value, by converting it
;;; into a list of key-value tuples and sorting on the value.
(define sort-by-value
  (lambda (table)
    (let ([keyval (hash-table-map table (lambda (key val) (list key val)))])
      (sort keyval (lambda (a b)
                     (< (cadr a) (cadr b)))))))


;;; add-bigrams
;;; <- list of strings, i.e. token list
;;; !-> updated hash-table bigram-hash
;;; !-> updated count-bigrams counter
;;; ----------------------------------------------------
;;; Add word-bigrams from an ordered list of tokens to the hash-table
;;; container and keep track of their count.
(define add-bigrams
  (lambda (words)
    (let ([count (- (length words) 1)])          ; how many bigrams
      (set! bigramcount (+ bigramcount count)) ; remember the total count
      (let loop ([i 1])
        (let* ([bigram (list (list-ref words (- i 1)) (list-ref words i))]  ; create bigram
               [value  (hash-table-get bigrams bigram 0.0)])             ; get the calue for bigram
          (hash-table-put! bigrams bigram (+ value 1)))
        (if (< i count)
            (loop (+ i 1)))))))


;;; load-file
;;; <- string filename
;;; -> string file content
;;; ----------------------------------------------------
;;; Load text from file into a string variable and return it.
(define load-file
  (lambda (name)
    (call-with-input-file name
      (lambda (p)
        (read-string (file-size name) p)))))


;;; main steps
(begin 
  (vector-for-each (lambda (i fname)
                     (let ([text (load-file fname)])
                       (string-lowercase! text) ; normalize the tokens to lowercase
                       ; replace punctuation marks in text before tokenization
                       (add-bigrams (string-tokenize (pregexp-replace* "[`'-.,!?;:<>()|\"\\]\\[$%/]+" text " ")))))
                   argv)
  (let ([result (sort-by-value bigrams)])
    (for-each (lambda (a)
                (let ([bigram (car a)])
                  (unless (or (member (car bigram) stopwords) (member (cadr bigram) stopwords))
                    (printf "~a ~a\t~a\n" (car bigram) (cadr bigram) (cadr a)))))
              (reverse result)))
  (printf "---------------------------------------------------------\n")
  (printf "Number of tokens\t~a\n" bigramcount)
  (printf "Number of types\t~a\n" (hash-table-count bigrams)))
