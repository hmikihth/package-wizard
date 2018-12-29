#!/usr/bin/python3
import subprocess

HAVE_SUMMARY = 'blackPanther OS' in subprocess.getoutput('cat /etc/os-release')
if not HAVE_SUMMARY:
    raw = subprocess.getoutput('LANG=en echo 1| pkcon -p get-details packagekit')
    HAVE_SUMMARY = '  summary:' in raw

PKCON_INFO_LINES = ['Name','Version','Release','Architecture'] + (['Summary']*HAVE_SUMMARY)
PKCON_INFO_LINES += ['License','Group','Description','Size','URL']

INFO_LINES = ['Name','Version','Release','Architecture','Summary','License','Group','Size','URL','Description']
DEB_ALIAS = {'Name':'Package', 'Size':'Installed-Size', 'URL':'Homepage', 'Group':'Section'}

def resolve_package(package):
    p = package.rfind('.')
    arch = package[p+1:]
    r = package[:p]
    p = r.rfind('-')
    release = r[p+1:]
    r = r[:p]
    p = r.rfind('-')
    version = r[p+1:]
    name = r[:p]
    return {'Name':name, 'Version':version, 'Release':release, 'Architecture':arch}

def get_rpm_file_info(filename):
    d = {e:'' for e in INFO_LINES}
    query = "rpm -qp " + filename + " --qf " + "'%{NAME}\\n%{VERSION}\\n%{RELEASE}\\n%{ARCH}\\n%{SUMMARY}\\n%{LICENSE}\\n%{GROUP}\\n%{SIZE}\\n%{URL}\\n%{DESCRIPTION}\\n'"
    print(query)
    raw = subprocess.getoutput(query)
    for i,e in enumerate(raw.split('\n')):
        if i<9:
            d[INFO_LINES[i]] = e
        else:
            d["Description"] += e + '\n'
    return d

def get_deb_file_info(filename):
    d = {e:'' for e in INFO_LINES}
    for e in INFO_LINES:
        if e in DEB_ALIAS:
            d[e] = subprocess.getoutput('dpkg -f ' + filename + ' ' + DEB_ALIAS[e])
        else:
            if e == 'Version':
                line = subprocess.getoutput('dpkg -f ' + filename + ' ' + e)
                p = line.rfind('-')
                d[e], d['Release'] = line[:p], line[p+1:]
            elif e not in ['Release']:
                d[e] = subprocess.getoutput('dpkg -f ' + filename + ' ' + e)
    if not d['Summary']:
        d['Summary'] = d["Description"][:100].strip()+'...'
    return d

def get_package_info(name):
    raw = subprocess.getoutput('echo 1| pkcon -p get-details '+name)
    d = {e:'' for e in PKCON_INFO_LINES}
    lines = raw.split('\n')
    for i,l in enumerate(lines):
        if l.startswith('  '):
            break
    lines = lines[i:]
    i = 0
    for l in lines:
        if i<=6+HAVE_SUMMARY or i>len(lines):
            if i == 0:
                d.update(resolve_package(l.split(':')[1].strip()))
                i = 3
            else:
                p = l.index(':')+1
                d[PKCON_INFO_LINES[i if i<=6+HAVE_SUMMARY else 6+HAVE_SUMMARY+i-len(lines)]] = l[p:].strip()
        else:
            if i>6+HAVE_SUMMARY:
                d["Description"] = '\n'.join([d["Description"], l])
        i+=1
    return d
    
if __name__ == "__main__":
#    print(get_rpm_file_info('../bcunit-devel-3.0.2-2bP.x86_64.rpm'))
    print(get_package_info('spyder'))
#    print(get_deb_file_info('spyder'))
#    print(resolve_package('bcunit-devel-3.0.2-2bP.x86_64'))
