.model small

.stack 100h

.data
      
    primerMensaje db "--- Productor Consumidor ---", "$"
       
    productor db "Productor: ", "$"
    consumidor db "Consumidor ", "$"
    bandera dw 0h ; 1 =  Productor, 2 = Consumidor
    
    activo db "Activo", "$"
    trabjando db "Trabajando", "$"
    dormido db "Dormido", "$"   
    
    disponible db ?
    buffer db 20 dup ("0")
    

.code

    mov ax, @data
    mov ds, ax 
    
    call menu
    
    mov ax, 04ch
    int 21h
    
    menu proc
        
        call menu
        
        cmp bandera, 01h
            call producir    
        
        
        menu endp
    
 
    producir proc
        
        mov ax, 02h
        
        ret
        
        producir endp

   rand proc
   
        push ax
        push cx
        push dx
   
        mov ah, 0h
        int 1Ah ; Obtener los ticks del reloj del sistema
        
        mov ax, dx
        xor dx, dx
        mov cx, 2
        div cx
        
        inc dx
        
        mov bandera, dx
        
        pop dx
        pop cx
        pop ax
        
        ret
   
    rand endp

end code
