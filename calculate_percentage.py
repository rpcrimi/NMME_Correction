import re

with open("NASA-GMAO_status.txt") as f:
	content = f.readlines()

m = re.compile("/.*\:")
r7 = re.compile(".*[0-9]{4}07.*")
r8 = re.compile(".*[0-9]{4}08.*")
r11 = re.compile(".*[0-9]{4}11.*")
ensembleRegex  = re.compile('.*r[0-9]+i[0-9]+p[0-9]+.*')

count = 0
july_nov_count = 0
for line in content:
	if re.match(m, line) and not re.match(ensembleRegex, line):
		count += 1	
		if re.match(r7, line) or re.match(r11, line) or re.match(r8, line):
			july_nov_count += 1
		else:
			print line

print july_nov_count, count