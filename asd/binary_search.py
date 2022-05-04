def binary_search(lys, val, key) :
  """
    Pencarian untuk list of dict.
  """
  first = 0
  last = len(lys) - 1
  row = -1

  while (first <= last) and (row == -1) :
    mid = (first + last) // 2

    if lys[mid][key] == val :
      row = mid
    else :
      if val < lys[mid][key] :
        last = mid - 1
      else:
        first = mid + 1
  
  return lys[mid]