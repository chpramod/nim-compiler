proc fibonacci(n: int): int =
  if n < 2:
    result = n
  else:
    result = fibonacci(n - 1) + fibonacci(n - 2)

echo fibonacci(5)
