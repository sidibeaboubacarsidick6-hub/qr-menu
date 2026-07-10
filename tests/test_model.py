import pytest
from django.contrib.auth.models import User
from apps.restaurants.models import Restaurant, QRCode
from apps.menus.models import Category, MenuItem


@pytest.mark.django_db
class TestRestaurant:
    
    def test_create_restaurant(self):
        user = User.objects.create_user(username='test_resto', password='test123')
        resto = Restaurant.objects.create(
            owner=user,
            name='Test Restaurant',
            slug='test-restaurant',
            is_active=True
        )
        assert resto.name == 'Test Restaurant'
        assert resto.slug == 'test-restaurant'
        assert resto.is_active is True
    
    def test_qr_code_generated(self):
        user = User.objects.create_user(username='test_resto2', password='test123')
        resto = Restaurant.objects.create(
            owner=user,
            name='Test QR',
            slug='test-qr'
        )
        qr = QRCode.objects.create(restaurant=resto)
        assert qr.restaurant == resto
        assert qr.uuid is not None
        assert '/m/' in qr.get_menu_url()


@pytest.mark.django_db
class TestMenu:
    
    def test_category_and_item(self):
        user = User.objects.create_user(username='test_resto3', password='test123')
        resto = Restaurant.objects.create(owner=user, name='Test Menu')
        cat = Category.objects.create(restaurant=resto, name='Entrées', order=1)
        item = MenuItem.objects.create(
            category=cat,
            name='Salade',
            price=9.99,
            is_vegetarian=True
        )
        assert cat.restaurant == resto
        assert item.category == cat
        assert item.price == 9.99
        assert item.is_vegetarian is True