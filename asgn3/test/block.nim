block outer:
  for i in 0..2000:
    for j in 0..2000:
      if i+j == 3145:
        echo i, ", ", j
        break outer

let b = 3
block:
  let b = "3"  # shadowing is probably a dumb idea
