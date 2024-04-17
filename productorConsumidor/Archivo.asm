.model small

.stack 100h

.data
      
    primerMensaje db "--- Productor Consumidor ---", 10, 13, "$"
    segundoMensaje db 10, 10, 13, "--- B U F F E R ----", 10, 10, 13, "$"
       
    productor db 10, , 13, "Productor: ", "$"
    consumidor db 10, 13, "Consumidor: ", "$"
    bandera dw 0h ; 1 =  Productor, 2 = Consumidor        
    
    activo db 09, "Activo", 10, 13, "$"
    trabajando db 09, "Trabajando",10, 13, "$"
    dormido db 09, "Dormido", 10, 13, "$"
    
    productorExito db 10, 10, 13,"Se ha producido: ", "$"
    consumidorExito db 10, 10, 13, "Se ha consumido: ", "$"
    numeroExito dw ?
    
    error db "No existen productos suficientes", "$"   
    
    disponible dw 0h
    buffer db 20 dup ("0")
    productorPtr dw 0h
    consumidorPtr dw 0h
    
.code

    mov ax, @data
    mov ds, ax 
    
    call menu
    
    mov ax, 04ch
    int 21h
    
    menu proc
        
        bucleMenu:
        
        mov ah, 09
        lea dx, primerMensaje
        int 21h
        
        mov bx, 01h
        call rand
        
        cmp bandera, 01h
            je producir
            
        cmp bandera, 02h
            je consumir
               
        producir:
            call produccion 
            jmp bucleMenu
        
        consumir:
            call consumision
            jmp bucleMenu        
               
        menu endp
    
    produccion proc
        
        push ax
        push bx
        push cx
        push dx
        push si
            
        mov ah, 09h
        lea dx, productor
        int 21h
        
        mov ah, 09h
        lea dx, activo
        int 21h
        
        mov ah, 09h
        lea dx, consumidor
        int 21h
        
        mov ah, 09h
        lea dx, dormido
        int 21h
        
        mov ah, 09h
        lea dx, segundoMensaje
        int 21h 
        
        mov ah, 09h
        lea dx, productor
        int 21h
        
        mov ah, 09h
        lea dx, trabajando
        int 21h
        
        mov bx, 02h
        call rand 
        
            xor si, si
            xor cx, cx
            mov si, productorPtr
        
            produccionBucle:
            
                mov buffer[si], "1"
                inc si
                inc cx
                
                add cx, disponible
           
                cmp cx, 13h
                    sub cx, disponible
                    je produccionLleno 
                     
                cmp si, 013h        
                    jne produccionFinal
                    xor si, si
                    
                produccionFinal:     
                
                    cmp cx, numeroExito
                        jl produccionBucle
                
                produccionLleno:        
                        
                        
             ; Almacenar la casilla donde la produccion termino           
                       
             mov productorPtr, si
             
             ; Actualizar la cantidad disponible de elementos para consumir
             
             mov ax, disponible
             add ax, numeroExito
             mov disponible, ax
             
             xor cx, cx
             xor si, si
               
             call impresion
             
             ; Indica cuantos elementos se producieron con exito
             
             mov ax, 09h
             lea dx, productorExito
             int 21h
             
             ; Adicionamos 48 Decimal para transformar la cantidad de bucles realizados en CX.
             
             add cl, "0"
             mov ah, 02h
             mov al, cl
             int 21h
                
         pop si
         pop dx
         pop cx
         pop bx
         pop ax
         
         ret 
                        
        produccion endp
    
    consumision proc
        
        push ax
        push bx
        push cx
        push dx
        push si
            
        mov ah, 09h
        lea dx, consumidor
        int 21h
        
        mov ah, 09h
        lea dx, activo
        int 21h 
        
        mov ah, 09h
        lea dx, productor
        int 21h
        
        mov ah, 09h
        lea dx, dormido
        int 21h
        
        mov ah, 09h
        lea dx, segundoMensaje
        int 21h 
        
        mov ah, 09h
        lea dx, consumidor
        int 21h
        
        mov ah, 09h
        lea dx, trabajando
        int 21h
        
        mov bx, 02h
        call rand 
        
            xor si, si
            xor cx, cx
            mov si, consumidorPtr
        
            consumicionBucle:
            
                mov buffer[si], "0"
                inc si
                inc cx
                
                sub cx, disponible
           
                cmp cx, 0h
                    add cx, disponible
                    je consumicionVacio 
                     
                cmp si, 013h        
                    jne consumicionFinal
                    xor si, si
                    
                consumicionFinal:     
                
                    cmp cx, numeroExito
                        jl consumicionBucle
                
                consumicionVacio:        
                        
                        
             ; Almacenar la casilla donde la produccion termino           
                       
             mov productorPtr, si
             
             ; Actualizar la cantidad disponible de elementos para consumir
             
             mov ax, disponible
             sub ax, numeroExito
             mov disponible, ax
             
             xor cx, cx
             xor si, si
               
             call impresion
             
             ; Indica cuantos elementos se producieron con exito
             
             mov ax, 09h
             lea dx, consumidorExito
             int 21h
             
             ; Adicionamos 48 Decimal para transformar la cantidad de bucles realizados en CX.
             
             add cl, "0"
             mov ah, 02h
             mov al, cl
             int 21h
                
         pop si
         pop dx
         pop cx
         pop bx
         pop ax
         
         ret 
                        
        consumision endp

   rand proc ; El rand tiene dos opciones 01 = BX retorna un numero random entre 1 y 2, 02 = BX retorna un numero random entre 4 - 7.
   
        push ax
        push bx
        push cx
        push dx 
   
        mov ah, 0h
        int 1Ah ; Obtener los ticks del reloj del sistema
        
        mov ax, dx ; Establecer los ticks en ax
        xor dx, dx
        
        cmp bx, 01h
        je primeraOpcion
        
        cmp bx, 02h
        je segundaOpcion 
            
            primeraOpcion:
            
                mov cx, 2h
                div cx 
                inc dx
                mov bandera, dx
                
                jmp final
            
            segundaOpcion:
            
                mov cx, 4h
                div cx
                add dx, 03h
                mov numeroExito, dx
                
                jmp final
           
        final:    
        
        pop dx
        pop cx
        pop bx
        pop ax
        
        ret
   
    rand endp 
   
   impresion proc ; Imprime los valores uno por uno, divide entre 5 para encontrar residuo 0, en dado caso \n para mantener una grilla.
    
    push ax
    push bx
    push si 
   
    xor ax, ax
    xor si, si
    
    mov ah, 02h
    
    impresionBucle:
    
        mov al, buffer[si]
        int 21h
                  
        inc si           
        xor ax, ax 
        mov ax, si
        mov bx, 05h
        
        div bx
       
        cmp si, 13h
            je impresionFinal
       
        cmp dx, 0h
            jne impresionBucle:
            
        mov al, 0Ah
        int 21h
        mov al, 0D
        int 21h
             
        jmp impresionBucle
        
    impresionFinal:
    
        pop si
        pop bx
        pop ax
        
        ret
  
    impresion endp

end code
