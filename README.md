# Create groups in django shell before start:
```python
from django.contrib.auth.models import Group
Group.objects.get_or_create(name='Subscriber')
Group.objects.get_or_create(name='Author')
```