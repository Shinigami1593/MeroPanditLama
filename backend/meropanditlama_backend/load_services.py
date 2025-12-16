#!/usr/bin/env python
"""
Load initial services data into the database.
Run: python manage.py shell < load_services.py
"""

from api.providers.models import Service

services = [
    {
        'name': 'Ghar Puja',
        'name_ne': 'घर पूजा',
        'description': 'House warming and purification ceremony for new homes',
        'description_ne': 'नयाँ घरको लागि घर वार्मिंग र शुद्धीकरण समारोह',
        'default_price': 3000
    },
    {
        'name': 'Bartabanda',
        'name_ne': 'बर्तबन्द',
        'description': 'Sacred thread ceremony for young boys (Bratabandha)',
        'description_ne': 'जवान केटाहरूको लागि पवित्र धागो समारोह',
        'default_price': 5000
    },
    {
        'name': 'Bratabandha',
        'name_ne': 'ब्रतबन्ध',
        'description': 'Coming of age ceremony and initiation ritual',
        'description_ne': 'उमेर आगमन समारोह र दीक्षा संस्कार',
        'default_price': 8000
    },
    {
        'name': 'Buddha Puja',
        'name_ne': 'बुद्ध पूजा',
        'description': 'Buddhist prayer and meditation ceremony',
        'description_ne': 'बौद्ध प्रार्थना र ध्यान समारोह',
        'default_price': 4000
    },
    {
        'name': 'Wedding Ceremony',
        'name_ne': 'विवाह समारोह',
        'description': 'Traditional Hindu or Buddhist wedding rituals and blessings',
        'description_ne': 'परम्परागत हिन्दू वा बौद्ध विवाह संस्कार र आशीर्वाद',
        'default_price': 15000
    },
    {
        'name': 'Griha Pravesh',
        'name_ne': 'गृह प्रवेश',
        'description': 'House entrance ceremony and blessings for new home',
        'description_ne': 'नयाँ घरको लागि घर प्रवेश समारोह र आशीर्वाद',
        'default_price': 4500
    },
    {
        'name': 'Funeral Rites',
        'name_ne': 'अन्त्येष्टि संस्कार',
        'description': 'Last rites and funeral ceremonies',
        'description_ne': 'अन्तिम संस्कार र अन्त्येष्टि समारोह',
        'default_price': 10000
    },
    {
        'name': 'Satyanarayan Puja',
        'name_ne': 'सत्यनारायण पूजा',
        'description': 'Worship of Lord Satyanarayan for prosperity',
        'description_ne': 'समृद्धिको लागि भगवान सत्यनारायणको पूजा',
        'default_price': 3500
    },
]

print("=" * 60)
print("Loading Services into Database...")
print("=" * 60)

created_count = 0
existing_count = 0

for service_data in services:
    service, created = Service.objects.get_or_create(
        name=service_data['name'],
        defaults=service_data
    )
    
    if created:
        print(f"✅ Created: {service.name} ({service.name_ne})")
        created_count += 1
    else:
        print(f"ℹ️  Already exists: {service.name}")
        existing_count += 1

print("=" * 60)
print(f"✅ Successfully loaded {created_count} new services!")
print(f"ℹ️  {existing_count} services already existed.")
print(f"📊 Total services in database: {Service.objects.count()}")
print("=" * 60)