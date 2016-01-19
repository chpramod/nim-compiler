#[ Multiline comment in already
   commented out code. ]#

echo "words words words ⚑"
echo """
<html\>
  <head>
  </head>\n\n

  <body>
  </body>
</html> """

proc re(s: system.string): system.string = s

echo r".""."
echo re"\b[a-z]++\b"