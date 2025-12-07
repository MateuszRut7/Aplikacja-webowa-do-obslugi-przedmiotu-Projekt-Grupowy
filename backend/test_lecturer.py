#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projekt_strony_backend.settings')
django.setup()

from users.models import AppUser
from groups.serializers import GroupSerializer

# Test 1: Sprawdź czy wykładowca istnieje
print("=== Test 1: Sprawdzenie wykładowców ===")
lecturers = AppUser.objects.filter(is_staff=True)
for l in lecturers:
    print(f"ID: {l.id}, Username: {l.username}, Name: {l.first_name} {l.last_name}")

# Test 2: Sprawdź serializer z ID
print("\n=== Test 2: Serializer z ID ===")
test_data = {
    "name_group": "Test Group",
    "lecturer": "23",  # ID jako string
    "topic": 42
}

serializer = GroupSerializer(data=test_data)
if serializer.is_valid():
    print("✓ Data is valid")
    print("Validated data:", serializer.validated_data)
    print("Lecturer object:", serializer.validated_data.get('lecturer'))
else:
    print("✗ Data is invalid")
    print("Errors:", serializer.errors)

# Test 3: Sprawdź serializer z username
print("\n=== Test 3: Serializer z username ===")
test_data2 = {
    "name_group": "Test Group 2",
    "lecturer": "prof_nowak",  # username
    "topic": 42
}

serializer2 = GroupSerializer(data=test_data2)
if serializer2.is_valid():
    print("✓ Data is valid")
    print("Validated data:", serializer2.validated_data)
    print("Lecturer object:", serializer2.validated_data.get('lecturer'))
else:
    print("✗ Data is invalid")
    print("Errors:", serializer2.errors)
