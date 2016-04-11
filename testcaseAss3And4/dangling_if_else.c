int main(void){
    int i = 0,a[]={1,2,3};
    if (i<=3)
        a[i]++;
    if (i>=2)
        a[i]--;
    else 
        a[i] = 1;
}

var i:int=0
var a:array[3,int]
a[1]=1
a[2]=2
a[3]=3
if i<=3:
  a[i] = a[i]+1
if i>=2:
  a[i] = a[i] -1
else:
  a[i]=1
