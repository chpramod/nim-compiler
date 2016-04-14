var a:int = 1
var b:int = -1
var c = 0    			#int not used
var d:int
echo "Enter your query,should be 1,-1 or 0\n"
scan d
case d:
  of 1:
    echo "Positive\n"
  of -1:
    echo "Negative\n"
  of 0:
    echo "Neutral\n"
  else:
    echo "Invalid Query\n"
