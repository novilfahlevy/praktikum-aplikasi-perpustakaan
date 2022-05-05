def merge_sort(lst, compare):
  if len(lst) <= 1 :
    return lst

  mid = len(lst) // 2

  left = merge_sort(lst[0:mid], compare)
  right = merge_sort(lst[mid:len(lst)], compare)
  
  return merge(left, right, compare)

def merge(left, right, compare) :
  result = []
  i, j = 0, 0

  while i < len(left) and j < len(right) :
    if compare(left[i], right[j]) :
      result.append(left[i])
      i += 1
    else :
      result.append(right[j])
      j += 1

  result += left[i:]
  result += right[j:]

  return result