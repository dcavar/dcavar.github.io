(define words (make-hash-table 'equal))
(hash-table? words)
(define word "Haus")
(hash-table-put! words word "house")
(hash-table-get words word)
; (hash-table-get words "house")
(hash-table-get words "house" "UNK")
(hash-table-put! words word 1)
(hash-table-put! words word (+ (hash-table-get words word 0) 1))
(hash-table-put! words "Garten" 1)
(hash-table-for-each words (lambda (key value)
                             (printf "~a\t~a\n" key value)))
