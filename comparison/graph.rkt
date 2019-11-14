#lang scheme 

( define city-map '(
    (chennai -> coimbatore madurai)
    (coimbatore -> salem trichy)  
    (madurai -> tanjore dindigul) ) )

(define (neighbours place graph)
    (cond        
            ((eq? '() graph) '())
            ((eq? place (caar graph)) (cddar graph))
            ('#t (neighbours place ( cdr graph)))))

(neighbours 'coimbatore city-map)
