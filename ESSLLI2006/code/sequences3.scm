(cons #\a 3)
'("hello" . 4)
;("hello" . 4)
(define touple (cons "Haus" 3))
(car touple)
(cdr touple)
(set-car! touple "house")
(set-cdr! touple (+ (cdr touple) 1))
touple
(define touple (cons (cons 4 1) "Haus"))
touple
(car (car touple))
(cdr (car touple))
(caar touple)
(cdar touple)