# создание уровней не в ручную

s = 's' * 8
t = '.' * 8

s_line = s * 6
s_t_line = s + t * 4 + s
print(len(s_line))

with open("data/lvl1.txt", "w") as file:
    for i in range(48):
        if i < 8 or i > 40:
            file.write(s_line + '\n')
        else:
            file.write(s_t_line + '\n')

