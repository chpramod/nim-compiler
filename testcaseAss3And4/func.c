int foo ()
{
    int i = 1;
    return 0;
}

int main(){
    int i = foo();
    return 0;
}

proc foo():int =
  var i:int=1
  return 0
var i:int
i=foo()
