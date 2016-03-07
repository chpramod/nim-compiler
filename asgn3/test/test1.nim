iterator items(range: int): int =
  var i = range.low
  while i <= range.high:
    yield i

iterator pairs(range: int): tuple[a: int, b: char] =
  for i in range:  # uses Range.items
    yield (i, char(i + ord('a')))

for i, c in TRange(low: 1, high: 3):
  echo c
iterator items(range: int): int =
  var i = range.low
  while i <= range.high:
    yield i
