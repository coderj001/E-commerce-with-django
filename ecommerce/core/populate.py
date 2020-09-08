import random

from core.models import Item
from django_seed import Seed

seeder = Seed.seeder()

seeder.add_entity(Item, 5, {
    'title': lambda x: "dummy {}".format(random.randint(0,1000)),
'price': lambda x: random.randint(100, 10000),
'discount_price ': lambda x: random.randint(1, 100),
'category ': lambda x: random.choices(['S','SW','OW'])[0],
'label ': lambda x: random.choices(['P','S','D'])[0]
})

inserted_pks = seeder.execute()
