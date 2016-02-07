.section .data

number:
  .long 73

primee:
  .ascii " is a prime number."

non_primee:
  .ascii " is not a prime number."

.section .text

.globl _start

_start:
  xorl %esi, %esi # esi for number of times the below loop executes
  movl number, %eax

loop: # eax stores quotient, edx stores remainder
  incl %esi
  movl $0, %edx
  movl $10, %ebx
  divl %ebx # quotient modulo 10
  addl $48, %edx # adding 48 to represtent the value as a ascii value
  pushl %edx # pushing the current least significant digit
  cmpl $0, %eax
  je _end
  jmp loop

_end:
  cmpl $0, %esi # to determine how mant times to runt he loop
  jz __start
  movl $4, %eax
  movl $1, %ebx
  movl %esp, %ecx # popping the current most significant digit
  movl $1, %edx
  int $0x80
  addl $4, %esp # incrementing the stact pointer to point to the next stack item
  decl %esi # decrementing the loop counter
  jmp _end

__start:
  pushl number
  call check_prime
  cmpl $1, %ebx
  je prime
  jmp non_prime
 
   prime:
    movl $primee, %ecx               # Location of the buffer
    movl $19, %edx # Size of the buffer
    jmp _exit

   non_prime:
    movl $non_primee, %ecx               # Location of the buffer
    movl $23, %edx # Size of the buffer
    jmp _exit

   _exit:
    movl $4, %eax                   # 4 is the system call number
    movl $1, %ebx                   # 1 stands for stdout
    int $0x80
    movl $1, %eax
    movl $0, %ebx
    int $0x80

.type check_prime, @function
check_prime: # prime check algorithm, checking divisibility with all possible factors
  pushl %ebp
  movl %esp, %ebp
  subl $32, %esp
  movl $2, %ebx
  start_loop:
    movl 40(%esp), %eax
    movl $0, %edx
    cmpl %eax, %ebx
    jge loop_exit
    divl %ebx
    cmpl $0, %edx # if equal non prime
    je loop_exit
    incl %ebx
    jmp start_loop

  loop_exit:
    cmpl $1, 40(%esp) # since we are saying 1 is non prime
    # je non_prime
    je non_primm
    cmpl 40(%esp), %ebx # prime check
    # jge prime
    jge primm
    # jmp non_prime
    jmp non_primm

  primm:
	movl %ebp, %esp
        popl %ebp
	movl $1, %ebx
	ret

  non_primm:
	movl %ebp, %esp
	popl %ebp
	movl $0, %ebx
	ret
