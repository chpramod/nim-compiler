proc positiveOrNegative(num: int): int =
  var a:int = 100
  var b:int = 100
  var c:int = 0
  case num:
    of 1:
      echo b
    of 0:
      echo c
    of 1:
      echo a
    else:
      a = a+1
  return positiveOrNegative(21)
