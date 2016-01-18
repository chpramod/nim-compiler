type
  Matrix[W, H: static[int]] =
    array[1..W, array[1..H, int]]

let mat1: Matrix[2, 2] = [[1, 0],
                          [0, 1]]
let mat2: Matrix[2, 2] = [[0, 1],
                          [1, 0]]

proc `+`[W, H](a, b: Matrix[W, H]):
               Matrix[W, H] =
  for i in 1..high(a):
    for j in 1..high(a[0]):
      result[i][j] = a[i][j] + b[i][j]

# See `$` from the procs section

echo mat1 + mat2