import string

def part1():
    f = open("input.txt")
    s = 0
    for line in f.readlines():
        digit_list = list(filter(lambda x: x not in string.ascii_letters, line.strip()))
        if len(digit_list) == 0:
            continue
        
        number = int(''.join(digit_list[0] + digit_list[-1]))
        s += number
    print(s)

def part2():
    f = open("input2.txt")
    out = open("debug.txt", "w")
    
    s = 0
    digit_map = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9
    }
    
    for line in f.readlines():
        line = line.strip()
        out.write(line + " | ")
        
        # Replace from left
        part = ""
        for c in line:
            part += c
            
            if c in string.digits:
                break
            
            for digit_str, digit_val in digit_map.items():
                if digit_str in part:
                    part = part.replace(digit_str, str(digit_val), 1)
        
        # Replace from right
        part_rev = ""
        for c in line[::-1]:
            part_rev += c
            
            if c in string.digits:
                break
            
            for digit_str, digit_val in digit_map.items():
                if digit_str in part_rev[::-1]:
                    part_rev = part_rev[::-1].replace(digit_str, str(digit_val), 1)[::-1]
        
        # Join
        line = part + part_rev[::-1]
        
        digit_list = list(filter(lambda x: x not in string.ascii_letters, line.strip()))
        if len(digit_list) == 0:
            continue
        
        number = int(''.join(digit_list[0] + digit_list[-1]))
        out.write(line + " | " + str(number) +  "\n")
        s += number
        
    print(s)

if __name__ == "__main__":
    part1()
    part2()
    