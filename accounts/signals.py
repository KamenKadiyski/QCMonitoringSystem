from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from django.db import IntegrityError, transaction

from .models import User, Employee

ROLE_MAP = {
    "machine operator": "operator",
    "qc inspector": "qc",
    "qc manager": "admin",
    "shift manager": "manager",
    "administrator": "admin",
}

@receiver(post_save, sender=Employee)
def create_user_for_employee(sender, instance, created, **kwargs):
    if not created or not instance.login_required or instance.user:
        return

    pre_username = slugify(f"{instance.first_name}.{instance.last_name}")
    username = pre_username
    i = 1

    work_position = instance.work_position.name.strip().lower()
    role = ROLE_MAP.get(work_position, "operator")

    email = f"{username}@whatmoreuk.com"
    temp_password = get_random_string(12)
    is_staff = role == "admin"


    while True:
        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=temp_password,
                    role=role,
                    is_staff=is_staff,
                )
            break
        except IntegrityError:
            i += 1
            username = f"{pre_username}{i}"

    instance.user = user
    instance.save(update_fields=["user"])
    send_mail(
        subject='New user system access credentials',
        message=f"Hello, {instance.first_name} {instance.last_name},\n\n"
                f"Your account has been created successfully.\n\n"
                f"Username: {username}\n"
                f"Temporary password: {temp_password}\n\n"
                f"Please log in and change your password.\n"
                f"You can use the nearest workstation.\n\n"
                f"Regards,\n"
                f"IT Department",
                from_email='noreply@whatmoreuk.com',
                recipient_list=['hr@whatmoreuk.com'],
                fail_silently=False,
                    )
