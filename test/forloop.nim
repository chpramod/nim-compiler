type
  TRange = object
    low: int
    high: int

iterator items(range: TRange): int =
  var i = range.low
  while i <= range.high:
    yield i
    inc i

iterator pairs(range: TRange): tuple[a: int, b: char] =
  for i in range:  # uses Range.items
    yield (i, char(i + ord('a')))

for i, c in TRange(low: 1, high: 3):
  echo c