var a:int
scan a
var i=0
var prev1=1
var prev2=1
var curr:int
echo prev1,"\n"
while i<a:
  echo prev2,"\n"
  curr = prev1 + prev2
  prev2 = prev1
  prev1 = curr
  inc i                     #incr used!
