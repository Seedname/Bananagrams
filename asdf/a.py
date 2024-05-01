with open('b.txt', 'r') as f:
    with open('a.txt', 'r') as g:
        times = g.readlines()
    names = f.readlines()
    names = [(names[i].strip(), list(map(int, times[i].strip().split(":")))) for i in range(len(names))]

final_names = {}
for name, time in names:
    if name not in final_names:
        final_names[name] = 0

    total_time = time[0] * 60 + time[1]
    final_names[name] += total_time

print(final_names)

