from users.models import AppUser
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token
import csv
import string
import random
from django.db import transaction
url = 'link do strony: http://localhost:8080/#/login'
csv.register_dialect('myDialect',
                     delimiter=';',
                     skipinitialspace=True,
                     quoting=csv.QUOTE_ALL)

with transaction.atomic():
    with open('usos.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, dialect='myDialect')
        for row in reader:
            if row[0] != 'indeks':
                password = ''
                name = row[0] + '_' + row[2] + '_' + row[1]
                u = AppUser(username=name)
                u.last_name = row[2]
                u.first_name = row[1]
                u.numer_index = row[0]
                for i in range(14):
                    chars = string.ascii_uppercase + string.digits
                    password = password + random.choice(chars)
                u.set_password(password)
                u.numer_index = row[0]
                u.save()
                group = Group.objects.get(name='student')
                group.user_set.add(u)
                Token.objects.create(user=u)
                file = open('./userfiles/' + name + ".txt", "w+")
                file.write('Zapraszamy na stronę przedmiotu PROJ1' + '\nnazwa użytkownika: ' + name + '\nhasło: '
                           + password + '\n' + url)
                group.save()
