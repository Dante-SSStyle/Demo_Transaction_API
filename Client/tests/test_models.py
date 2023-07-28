from Client.models import ExtendedUser
from django.test import TestCase


class UsersTestCase(TestCase):
    def setUp(self):
        ExtendedUser.objects.create(username="TestUser1", password="pass")
        ExtendedUser.objects.create(username="TestUser2", password="pass", ITN=1010101010, balance=100)

    def test_users(self):
        user1 = ExtendedUser.objects.get(username="TestUser1")
        user2 = ExtendedUser.objects.get(username="TestUser2")

        self.assertEqual(user1.__str__(), f"{user1.username}: ИНН не указан.", "Check __str__ for user1")
        self.assertEqual(user1.balance, 0.00, "Check balance for user1")
        self.assertEqual(user2.__str__(), f"{user2.username}: {user2.ITN}", "Check __str__ for user2")
        self.assertEqual(user2.balance, 100.00, "Check balance for user2")
