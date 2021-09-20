from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from cart.cart import Cart
from account.models import Profile
from .models import Category, Product, Size, SizeType

User = get_user_model()


class ShopTestCase(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(username='test', password='test')
        self.profile = Profile.objects.create(user_id=1,
                                              phone='+375297875473',
                                              city='Grodno',
                                              postal_code='230020')
        self.category = Category.objects.create(name='Football Boots',
                                                slug='football-boots')
        self.sizetype = SizeType.objects.create(name='Size Shoes')
        self.product = Product.objects.create(
            category=self.category,
            sizetype=self.sizetype,
            name='test boots',
            slug='test-boots',
            price=Decimal('100')
        )

    def test_user_profile(self):
        customer = self.user.profile
        self.assertEqual(customer.phone, '+375297875473')
        self.assertEqual(customer.city, 'Grodno')
        self.assertEqual(customer.postal_code, '230020')

    def test_product_fields(self):
        boots = self.product
        self.assertEqual(boots.sizetype.name, 'Size Shoes')
        self.assertEqual(boots.category.name, 'Football Boots')