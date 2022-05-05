def binary_search(lys, val, atribut) :
  """
    Pencarian untuk list of dict.
  """
  first = 0
  last = len(lys) - 1
  row = -1

  while (first <= last) and (row == -1) :
    mid = (first + last) // 2

    if getattr(lys[mid], atribut) == val :
      row = mid
    else :
      if val < getattr(lys[mid], atribut) :
        last = mid - 1
      else:
        first = mid + 1
  
  return lys[mid]