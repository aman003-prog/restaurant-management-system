from decimal import Decimal
from datetime import timedelta
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from apps.categories.models import Category
from apps.menu.models import MenuItem
from apps.cart.models import Cart

User = get_user_model()

class CartAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword123"
        )
        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(
            title="Pizzas",
            description="Delicious pizzas"
        )
        self.menu_item = MenuItem.objects.create(
            title="Margherita Pizza",
            description="Cheese & tomato",
            price=Decimal("12.50"),
            category=self.category,
            available=True,
            preparation_time=timedelta(minutes=15),
            calories=650.0
        )
        self.menu_item2 = MenuItem.objects.create(
            title="Veggie Burger",
            description="Crispy patty",
            price=Decimal("8.00"),
            category=self.category,
            available=True,
            preparation_time=timedelta(minutes=10),
            calories=450.0
        )

    def test_add_item_to_cart(self):
        response = self.client.post("/api/cart/", {"menu_item": self.menu_item.id, "quantity": 1}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cart.objects.filter(user=self.user).count(), 1)
        item = Cart.objects.get(user=self.user)
        self.assertEqual(item.quantity, 1)
        self.assertEqual(item.unit_price, Decimal("12.50"))
        self.assertEqual(item.price, Decimal("12.50"))

    def test_increase_quantity_by_adding_same_product(self):
        # First add with quantity 1
        res1 = self.client.post("/api/cart/", {"menu_item": self.menu_item.id, "quantity": 1}, format="json")
        self.assertEqual(res1.status_code, status.HTTP_201_CREATED)

        # Second add same item with quantity 2
        res2 = self.client.post("/api/cart/", {"menu_item": self.menu_item.id, "quantity": 2}, format="json")
        print("Response 2:", res2.status_code, res2.data if hasattr(res2, 'data') else None)
        self.assertEqual(Cart.objects.filter(user=self.user).count(), 1)
        item = Cart.objects.get(user=self.user)
        self.assertEqual(item.quantity, 3)
        self.assertEqual(item.price, Decimal("37.50"))

    def test_update_cart_item_quantity(self):
        item = Cart.objects.create(
            user=self.user,
            menu_item=self.menu_item,
            quantity=1,
            unit_price=self.menu_item.price,
            price=self.menu_item.price
        )
        # PATCH quantity to 5
        response = self.client.patch(f"/api/cart/{item.id}/", {"quantity": 5}, format="json")
        print("PATCH response:", response.status_code, response.data if hasattr(response, 'data') else None)
        item.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(item.quantity, 5)
        self.assertEqual(item.price, Decimal("62.50"))

    def test_delete_cart_item(self):
        item = Cart.objects.create(
            user=self.user,
            menu_item=self.menu_item,
            quantity=1,
            unit_price=self.menu_item.price,
            price=self.menu_item.price
        )
        response = self.client.delete(f"/api/cart/{item.id}/")
        print("DELETE item response:", response.status_code)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Cart.objects.filter(user=self.user).count(), 0)

    def test_clear_cart(self):
        Cart.objects.create(
            user=self.user,
            menu_item=self.menu_item,
            quantity=1,
            unit_price=self.menu_item.price,
            price=self.menu_item.price
        )
        Cart.objects.create(
            user=self.user,
            menu_item=self.menu_item2,
            quantity=2,
            unit_price=self.menu_item2.price,
            price=self.menu_item2.price * 2
        )
        response = self.client.delete("/api/cart/")
        print("Clear cart response:", response.status_code)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Cart.objects.filter(user=self.user).count(), 0)
