import re

lista_url = ['http://www.aaa.es',
    'ftp://www.aaa.es',
    'http://www.bbb.es']
for elemento in lista_url:
    if re.search('es$', elemento):
        print(elemento)