def decrypt_character(last, current):
    last = last * current % 95
    return last + 32 if last != 0 else 33

def decrypt(data):
    result = ""
    offset = 0
    last = 60
    while offset < len(data):
        current = ord(data[offset])
        if current == last:
            ahead = ord(data[offset + 1])
            if ahead != last:
               _loc7_ = (ahead - 32) * 95 + ord(data[offset + 2]) - 32
               if _loc7_ == 0:
                  last = decrypt_character(last, 61)
                  offset += 3
                  continue
               _loc5_ = ord(data[offset + 3]) - 27
               result += result[len(result) - _loc7_ - _loc5_:len(result) - _loc7_]
               last = decrypt_character(last, ord(result[len(result) - _loc5_]))
               offset += 2
            else:
               result += chr(last)
               last = decrypt_character(last, last)
            offset += 2
        else:
            result += chr(current)
            offset += 1
    return result
