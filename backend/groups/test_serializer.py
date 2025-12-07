# Testowanie serializatora
from groups.models import Group
from groups.serializers import GroupSerializer

# Sprawdźmy jak serializer działa
print("Testing GroupSerializer...")

# Tworzymy przykładowe dane
test_data = {
    "name_group": "Test Group",
    "lecturer": 23,  # ID wykładowcy
    "topic": 42      # ID tematu
}

# Sprawdzamy walidację
serializer = GroupSerializer(data=test_data)
if serializer.is_valid():
    print("✓ Test data is valid")
    print("Validated data:", serializer.validated_data)
else:
    print("✗ Test data is invalid")
    print("Errors:", serializer.errors)
