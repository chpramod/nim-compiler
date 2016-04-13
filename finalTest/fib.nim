proc foo(a:int):int =
  if a == 0:
    return 1
  if a == 1:
    return 1
  else :
    var b,f,g,h,i:int
    h=a-1
    i=a-2
    b = foo(h)
    f= foo(i)
    g = b + f
    return g
var c:int
c = foo(2)
echo c
