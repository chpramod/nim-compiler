.section .data

input_str_begin:
  .ascii "Hello World"
input_str_end:

.section .text

.globl _start

_start: # initializing the registers for the loop
  pushl $(input_str_end-1)
  pushl $input_str_begin
  call reverse_string
  jmp loop_exit

  loop_exit: # printing the reverse string
    movl $4, %eax                   # 4 is the system call number
    movl $1, %ebx                   # 1 stands for stdout
    movl $input_str_begin, %ecx               # Location of the buffer
    movl $(input_str_end - input_str_begin), %edx # Size of the buffer
    int $0x80

    movl $1, %eax
    movl $0, %ebx
    int $0x80

.type reverse_string, @function
reverse_string: # swapping loop
    pushl %ebp
    movl %esp, %ebp
    movl 8(%esp), %eax
    movl 12(%esp), %ebx
    start_loop:
        cmpl %eax, %ebx
        jle exit
        movb (%eax), %cl # using 8 bit registers for characters
        movb (%ebx), %dl
        xorb %cl, %dl # xor swapping algorithm
        xorb %dl, %cl # xor swapping algorithm
        xorb %cl, %dl # xor swapping algorithm
        movb %cl, (%eax)
        movb %dl, (%ebx)
        incl %eax
        decl %ebx
        jmp start_loop
    exit:
	movl %ebp, %esp
	popl %ebp
        ret
