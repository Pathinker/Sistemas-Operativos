.model small

.stack 100h

.data
      
    primerMensaje db "--- Productor Consumidor ---" 10, 13, "$"
    segundoMensaje db 10, 10, 13, "--- B U F F E R ----" 10, 10, 13, "$"
       
    productor db 10, , 13 "Productor: ", "$"
    consumidor db 10, 13"Consumidor: ", "$"
    bandera dw 0h ; 1 =  Productor, 2 = Consumidor
    
    activo db 09, "Activo", 10, 13, "$"
    trabajando db 09, "Trabajando",10, 13, "$"
    dormido db 09, "Dormido", 10, 13, "$"
    
    productorExito db "Se ha producido: ", "$"
    consumidorExito db "Se ha consumido: ", "$"
    numeroExito dw ?
    
    error db "No existen productos suficientes", "$"   
    
    disponible db 14h
    buffer db 20 dup ("0")
    bufferPtr db 0h
    
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
            call consumicion
            jmp bucleMenu        
               
        menu endp
    
    produccion proc
        
        mov ax, 09h
        lea dx, productor
        int 21h
        
        mov ax, 09h
        lea dx, activo
        
        mov ax, 09h
        lea dx, consumidor
        int 21h
        
        mov ax, 09h
        lea dx, dormido
        int 21h 
        
        mov ax, 09h
        lea dx, productor
        int 21h
        
        mov ax, 09h
        lea dx, trabajando
        int 21h
        
        mov bx, 02h
        call rand 
        
            xor si, si
            xor cx, cx
            mov si, bufferPtr
        
            produccionBucle:
            
                mov buffer[si], "1"
                inc si
                inc cx
                
                cmp cx, numeroExito
                    jl produccionBucle
                
             mov bufferPtr, si
             xor cx, cx
             xor si, si
               
             call impresion 
                        
        producir endp

   rand proc
   
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
            
            primerOpcion:
            
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
   
   impresion proc
    
    ; Seccion donde se mostrara el buffer con los datos remanentes
    
    impresion endp

end code
