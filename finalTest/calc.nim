var a:int
var b:int
var res:int
var c:char='a'
while c!='!':
  echo "Enter your first number\n"
  scan a
  echo "Enter your second number\n"
  scan b
  echo "Operation you want to perform?\n"
  scan c
  if c=='*':
    res=a*b
  elif c=='+':
    res=a+b
  elif c=='-':
    res=a-b
  elif c=='/':
    res=a-b
  else:
    echo "Invalid operation"
    continue
  echo res
