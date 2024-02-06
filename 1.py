sus = "n, n^2, n^3"

for i in range(1,101):
    sus = sus + f"\n{i} {i**2} {i**3}"

with open(".txt", "w") as f:
    f.write(sus)