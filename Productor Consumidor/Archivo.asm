.model small

.stack 100h

.data
      
    primerMensaje db "--- Productor Consumidor ---", 10, 13, "$"
    segundoMensaje db 10, 10, 13, "--- B U F F E R ----", 10, 10, 13, "$"
       
    productor db 10, 13, "Productor: ", "$"
    consumidor db 10, 13, "Consumidor: ", "$"
    bandera dw 0h ; 1 =  Productor, 2 = Consumidor        
    
    activo db 09, "Activo", 10, 13, "$"
    trabajando db 09, "Trabajando", "$"
    dormido db 09, "Dormido", 10, 13, "$"
    
    productorExito db 10, 10, 13,"Se ha producido: ", "$"
    consumidorExito db 10, 10, 13, "Se ha consumido: ", "$"
    numeroExito dw ?
    
    teclado db 0h     
    disponible dw 0h
    buffer db 20 dup ("0")
    productorPtr dw 0h
    consumidorPtr dw 0h
    contadorAuxiliar db 0h
    
.code

    mov ax, @data
    mov ds, ax 
    
    call menu
    
    mov ax, 04ch
    int 21h
    
    menu proc
        
        bucleMenu:
        
        call kbhit
        
        cmp teclado, 01h
            je terminarMenu
        
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
            
        terminarMenu:
            
            ret
                               
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
        
        mov ah, 02h
        mov dx, 028h
        int 21h
        
        mov ah, 02h
        mov dx, numeroExito
        add dx, "0"
        int 21h
        
        mov ah, 02h
        mov dx, 029h
        int 21h 
        
        mov ah, 02h
        mov dl, 0AH
        int 21h
                
        mov ah, 02h
        mov dl, 0AH
        int 21h
        
        mov ah, 02h
        mov dl, 0DH
        int 21h
        
            xor si, si
            xor cx, cx
            mov si, productorPtr
        
            produccionBucle:
            
                mov dx, disponible
                add dx, cx
           
                cmp dx, 014h
                    je produccionLleno 
            
                mov buffer[si], "1"
                inc si
                inc cx
                
                cmp si, 014h        
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
             add ax, cx
             mov disponible, ax
               
             call impresion
             
             ; Indica cuantos elementos se producieron con exito
             
             mov ah, 09h
             lea dx, productorExito
             int 21h
             
             ; Adicionamos 48 Decimal para transformar la cantidad de bucles realizados en CX.
             
             mov ah, 02h
             add cl, "0"
             mov dl, cl
             int 21h
             
             call esperar
             
             call limpiarPantalla 
             
             xor cx, cx
             xor si, si
                
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
        
        mov ah, 02h
        mov dx, 028h
        int 21h
        
        mov ah, 02h
        mov dx, numeroExito
        add dx, "0"
        int 21h
        
        mov ah, 02h
        mov dx, 029h
        int 21h 
        
        mov ah, 02h
        mov dl, 0AH
        int 21h
                
        mov ah, 02h
        mov dl, 0AH
        int 21h
        
        mov ah, 02h
        mov dl, 0DH
        int 21h
        
            xor si, si
            xor cx, cx
            mov si, consumidorPtr
        
            consumicionBucle:
            
                mov dx, disponible
                sub dx, cx
           
                cmp dx, 0h
                    je consumicionVacio 
                     
                mov buffer[si], "0"
                inc si
                inc cx
                
                cmp si, 014h        
                    jne consumicionFinal
                    xor si, si
                    
                consumicionFinal:     
                
                    cmp cx, numeroExito
                        jl consumicionBucle
                
                consumicionVacio:        
                        
                        
             ; Almacenar la casilla donde la produccion termino           
                       
             mov consumidorPtr, si
             
             ; Actualizar la cantidad disponible de elementos para consumir
             
             mov ax, disponible
             sub ax, cx
             mov disponible, ax
             
             call impresion
             
             ; Indica cuantos elementos se producieron con exito
             
             mov ah, 09h
             lea dx, consumidorExito
             int 21h
             
             ; Adicionamos 48 Decimal para transformar la cantidad de bucles realizados en CX.
             
             mov ah, 02h
             add cl, "0"
             mov dl, cl
             int 21h
              
             call esperar
             call limpiarPantalla
             
             xor cx, cx
             xor si, si
                
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
                add dx, 04h
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
        push dx
        push si 
       
        xor si, si
        
        impresionBucle:
        
            xor ax, ax
            mov ah, 02h
            mov dl, buffer[si]
            int 21h
                      
            inc si           
            xor ax, ax
            xor dx, dx 
            mov ax, si
            mov bx, 05h
            
            div bx
           
            cmp si, 14h
                je impresionFinal
           
            cmp dx, 0h
                jne impresionBucle:
           
            mov ah, 02h
            mov dl, 0Dh
            int 21h     
            mov dl, 0Ah
            int 21h
                 
            jmp impresionBucle
            
        impresionFinal:
        
            pop si
            pop dx
            pop bx
            pop ax
            
            ret
  
    impresion endp
   
   proc limpiarPantalla
    
        push ax
    
        mov ax, 03h
        int 10h
    
        pop ax
    
        ret
    
   endp limpiarPantalla
   
   proc esperar ; Obtengo el tiempo de mi maquina y espero 3 segundos despues de ello, para eso almaceno su valor y lo aumento 3, en caso de ser mayor a 60 resto la misma cantidad.
    
        push ax
        push bx
        push cx
        push dx
        
        mov ah, 2Ch ; Obtener hora del sistema, CH -> Hora, CL -> Minuto, Dh -> Segundos, Dl -> Centesimas
        int 21h ;
            
        add dh, 05h    
        mov contadorAuxiliar, dh
              
        cmp contadorAuxiliar, 03Ch 
        jl esperarBucle
        sub dh, 03Ch
        mov contadorAuxiliar, dh
        
        esperarBucle: ; Es almacenado el segundo y se compara 
        
            mov ah, 02ch
            int 21h
            
            cmp dh, contadorAuxiliar
            jne esperarBucle 
            
        pop dx
        pop cx
        pop bx
        pop ax
        
        ret
    
   endp esperar
   
   kbhit proc ; Validar si se ha presionado una tecla, para finalizar el programa
        
        push ax
        xor ax, ax
        
        mov ah, 01h 
        int 16h     ; Leer teclado
    
        jnz teclaPresionada  
    
        mov teclado, 0h 
        pop ax
        
        ret
    
            teclaPresionada:
            
                mov teclado, 01h ; Tecla presionada
                pop ax
                
                ret

       kbhit endp

end code
