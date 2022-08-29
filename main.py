y = 2345
d28 = [2]
d30 = [4,6,9,11]
date = []

for m in range(1,13):
    if m in d28:
        for d in range(1,29):
            date = []
            if d < 10: date.append('0')
            for da in str(d): date.append(da)
            if m < 10: date.append('0')
            for mo in str(m): date.append(mo)
            for ye in str(y): date.append(ye)
            if len(date) == len(set(date)): print(date)
    if m in d30:
        for d in range(1,31):
            date = []
            if d < 10: date.append('0')
            for da in str(d): date.append(da)
            if m < 10: date.append('0')
            for mo in str(m): date.append(mo)
            for ye in str(y): date.append(ye)
            if len(date) == len(set(date)): print(date)
    else:
        for d in range(1,32):
            date = []
            if d < 10: date.append('0')
            for da in str(d): date.append(da)
            if m < 10: date.append('0')
            for mo in str(m): date.append(mo)
            for ye in str(y): date.append(ye)
            if len(date) == len(set(date)): print(date)
