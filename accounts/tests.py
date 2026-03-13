from django.test import TestCase
from django.core import mail
from django.contrib.auth import get_user_model
from .models import Employee, WorkPosition

User = get_user_model()
# Create your tests here.
class EmployeeSignalTest(TestCase):
    def setUp(self):
        # Създаваме различни позиции за тест на ROLE_MAP
        self.pos_qc = WorkPosition.objects.create(name="QC Inspector")
        self.pos_admin = WorkPosition.objects.create(name="Administrator")
        self.pos_other = WorkPosition.objects.create(name="Cleaner")

    def test_user_creation_with_correct_role_and_slug(self):
        """Проверка за автоматично създаване на User, роля и username slug"""
        emp = Employee.objects.create(
            first_name="Ivan",
            last_name="Ivanov",
            clock_number="1001",
            work_position=self.pos_qc,
            login_required=True
        )

        self.assertIsNotNone(emp.user)
        self.assertEqual(emp.user.username, "ivan-ivanov")
        self.assertEqual(emp.user.role, "qc")
        self.assertFalse(emp.user.is_staff)
        # Проверка на имейла в опашката
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("ivan-ivanov", mail.outbox[0].body)

    def test_is_staff_assignment_for_admin_role(self):
        """Проверка дали роля 'admin' получава is_staff=True"""
        emp = Employee.objects.create(
            first_name="Admin",
            last_name="User",
            clock_number="9999",
            work_position=self.pos_admin,
            login_required=True
        )
        self.assertTrue(emp.user.is_staff)
        self.assertEqual(emp.user.role, "admin")

    def test_username_collision_handling(self):
        """Проверка дали се справя с дублиращи се имена (итерация на username)"""
        # Първи потребител
        Employee.objects.create(
            first_name="John", last_name="Doe",
            clock_number="J1", work_position=self.pos_other, login_required=True
        )
        # Втори потребител със същото име
        emp2 = Employee.objects.create(
            first_name="John", last_name="Doe",
            clock_number="J2", work_position=self.pos_other, login_required=True
        )

        self.assertEqual(emp2.user.username, "john-doe2")

    def test_no_login_no_user(self):
        """Проверка, че не се създава User, ако login_required е False"""
        emp = Employee.objects.create(
            first_name="No",
            last_name="Login",
            clock_number="0000",
            work_position=self.pos_other,
            login_required=False
        )
        self.assertIsNone(emp.user)
        self.assertEqual(len(mail.outbox), 0)

    def test_default_role_mapping(self):
        """Проверка дали непозната позиция получава роля 'operator' по подразбиране"""
        emp = Employee.objects.create(
            first_name="Unknown",
            last_name="Position",
            clock_number="5555",
            work_position=self.pos_other,
            login_required=True
        )
        self.assertEqual(emp.user.role, "operator")
