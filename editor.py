def multiple_replace(target_str, replace_values):
  for i, j in replace_values.items():
    target_str = target_str.replace(i, j)
  return target_str

def to_weird_case(string):
  return ''.join(
    [c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(string)])