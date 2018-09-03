#!/usr/bin/env python3
#
# explore packages stats
import sys
import os
import time
import json

def main():
    start = time.time()

    # db = 'pypilist.json.bak'
    db = os.path.join(os.path.expanduser('~'), 'microrepo', 'packages.json')
    with open(db) as r:
        # packages = yaml.load(r.read().replace('\t',' ').replace('\n',' '))
        packages = json.load(r)
    
    total = 0
    combinations = {}
    pyversions = {}
    packagetypes = {}
    extensions = {}
    table = {}
    for package in packages:
        total += 1
        info = package['info']
        name = info['name']
        author = info['author']
        email = info['author_email']
        version = info['version']
        summary = info['summary']
        urls = package['urls']
        releases = package['releases']
        for url in urls:
            extension = url['filename'].split('.')[-1]
            if extension not in extensions:
                extensions[extension] = extension
            packagetype = url['packagetype']
            if packagetype not in packagetypes:
                packagetypes[packagetype] = packagetype
            python_version = url['python_version']
            if python_version not in pyversions:
                pyversions[python_version] = python_version

            key = '%s %s %s' % (python_version, packagetype , extension)
            if key not in combinations:
                combinations[key] = [url['filename'],0]
            combinations[key][1] += 1

        # 'author,email,version,size,summary,
        # oldest,newest,downloads'
        if not author: 	author = ''
        if not summary:	summary = ''
        if not email:	email = ''
        if ',' in author: 	author = author.replace(',',';')
        if '"' in author: 	author = author.replace('"','\'')
        if ',' in summary:	summary = summary.replace(',',';')
        if '"' in summary: 	summary = summary.replace('"','\'')
        if ',' in email:	email = email.replace(',',';')
        if '"' in email: 	email = email.replace('"','\'')
        
        table[name]=[author[:50],email[:50],summary[:100],version,0,"2100-01-01","1900-01-01",0]

        for ver,rlist in releases.items():
            for rel in rlist:
                r = table[name]				
                if not r[4] and ver == version:
                    r[4] = rel['size']
                if rel['upload_time'] < r[5]:
                    r[5] = rel['upload_time']
                if rel['upload_time'] > r[6]:
                    r[6] = rel['upload_time']
                r[7] += rel['downloads']



    print("Total packages:", total)
    print("Pyton versions:", sorted(pyversions))
    print("Package types:", sorted(packagetypes))
    print("Extensions:", sorted(extensions))
    
    print("Combinations:")

    i = 0
    for t in sorted(combinations):
        i += 1
        print('%3d) %-30s [packages: %6d]' % (i, t, combinations[t][1]))
        # print('%s,%s,%s' % (i, t, combinations[t][1]))

    header = 'name,author,email,summary,version,size,oldest,newest,downloads\n'
    with open('packages.csv','w') as w:
        w.write(header)
        for name, r in table.items():
            if r[7]>0:
                line = '"%s","%s","%s","%s","%s",%s,%s,%s,%s\n' % (name, r[0],r[1],r[2],r[3],r[4],r[5],r[6],r[7])
                # print (line)
                w.write(line.encode('utf-8'))
                # break			
    print('time:', (time.time()-start))




if __name__ == '__main__':
    main()