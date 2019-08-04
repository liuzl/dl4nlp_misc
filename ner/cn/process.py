lines = [line.strip() for line in open('199806.txt').read().split('\n') if line.strip() != '']
# len(lines)=21143
out = open('sample.train','w')
for line in lines[:10000]:
    for item in line.split()[1:]:
        if len(item.split('/')) != 2: item = '/'.join(item.split('/')[:2])
        out.write(item.replace('/', '\t')+"\n")
    out.write('EOS\n')
out.close()

out = open('sample.dev','w')
for line in lines[10000:20000]:
    for item in line.split()[1:]:
        if len(item.split('/')) != 2: item = '/'.join(item.split('/')[:2])
        out.write(item.replace('/', '\t')+"\n")
    out.write('EOS\n')
out.close()

out = open('sample.test','w')
for line in lines[20000:]:
    for item in line.split()[1:]:
        if len(item.split('/')) != 2: item = '/'.join(item.split('/')[:2])
        out.write(item.replace('/', '\t')+"\n")
    out.write('EOS\n')
out.close()
