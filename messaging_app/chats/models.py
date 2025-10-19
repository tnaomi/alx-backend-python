from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .validators import validate_date_of_birth, validate_phone_number


class Role(models.Model):
    """Role model to define user roles in the messaging app.

    Args:
        models (Model): Django Model class
    """
    role_id = models.CharField(max_length=50, primary_key=True, default=uuid4, editable=False, serialize=False, auto_created=True)
    name = models.CharField(max_length=50, unique=True, null=False, blank=False, serialize=True, error_messages={
        "unique": _("A role with that name already exists."),
        "blank": _("Role name is required.")})
    description = models.TextField(null=True, blank=True, serialize=True)

    # audit fields
    created_at = models.DateTimeField(auto_now_add=True, serialize=False, editable=False)
    updated_at = models.DateTimeField(auto_now=True, serialize=False, editable=True)
    deleted_at = models.DateTimeField(null=True, blank=True, serialize=False, editable=True)

    created_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='creator_role', serialize=False)
    updated_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='updater_role', serialize=False)
    deleted_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='deleter_role', serialize=False)

    def __str__(self):
        return self.name.capitalize()

class User(AbstractUser):
    """Custom `User` model to extend AbstractUser

    Args:
        AbstractUser (_type_): _Abstract User model_
    """
    user_id = models.CharField(max_length=50, primary_key=True, default=uuid4,editable=False,serialize=False,auto_created=True)
    date_of_birth = models.DateField(_("Please enter your date of birth"),null=False, blank=False, serialize=True,validators=[validate_date_of_birth], error_messages={
        "blank": _("Date of birth is required.")})
    password_hash = models.CharField(max_length=128, null=False, blank=False, serialize=False)
    phone_number = models.CharField(max_length=15, null=False, unique=True, blank=False, serialize=True, validators=[validate_phone_number], help_text="Phone number in international format, e.g., +265123456789", error_messages={
        "unique": _("A user with that phone number already exists."),
        "blank": _("Phone number is required.")})
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=False, blank=False, serialize=True)
    # audit fields
    created_at = models.DateTimeField(auto_now_add=True, serialize=False, editable=False)
    updated_at = models.DateTimeField(auto_now=True, serialize=False, editable=True)
    deleted_at = models.DateTimeField(null=True, blank=True, serialize=False, editable=True)

    created_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='creator_user', serialize=False)
    updated_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='updater_user', serialize=False)
    deleted_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='deleter_user', serialize=False)
    
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'date_of_birth', 'role']

    def __str__(self):
        return self.get_full_name().capitalize()

    def save(self, *args, **kwargs):
        # Hash the password before saving
        if self.password:
            from django.contrib.auth.hashers import make_password
            self.password_hash = make_password(self.password)
            self.password = self.password_hash
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-created_at']

class Message(models.Model):
    """Message model to store messages between users.

    Args:
        models (Model): Django Model class
    """
    message_id = models.CharField(max_length=50, primary_key=True, default=uuid4, editable=False, serialize=False, auto_created=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages', serialize=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', serialize=True)
    message_body = models.TextField(null=False, blank=False, serialize=True)
    sent_at = models.DateTimeField(auto_now_add=True, serialize=False, editable=False)
    conversation = models.ForeignKey('Conversation', on_delete=models.CASCADE, related_name='messages', null=True, blank=True)


    # audit fields
    created_at = models.DateTimeField(auto_now_add=True, serialize=False, editable=False)
    updated_at = models.DateTimeField(auto_now=True, serialize=False, editable=True)
    deleted_at = models.DateTimeField(null=True, blank=True, serialize=False, editable=True)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='creator_message', serialize=False)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='updater_message', serialize=False)
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='deleter_message', serialize=False)

    def __str__(self):
        return f"Message from {self.sender.get_full_name()} to {self.receiver.get_full_name()}"

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ['-created_at']

class Conversation(models.Model):
    """Conversation model to group messages between users.

    Args:
        models (Model): Django Model class
    """
    conversation_id = models.CharField(max_length=50, primary_key=True, default=uuid4, editable=False, serialize=False, auto_created=True)
    participants = models.ManyToManyField(User, related_name='conversations', serialize=True)
    created_at = models.DateTimeField(auto_now_add=True, serialize=False, editable=False)

    # audit fields
    updated_at = models.DateTimeField(auto_now=True, serialize=False, editable=True)
    deleted_at = models.DateTimeField(null=True, blank=True, serialize=False, editable=True)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='creator_conversation', serialize=False)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='updater_conversation', serialize=False)
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='deleter_conversation', serialize=False)

    def __str__(self):
        return f"Conversation {self.conversation_id}"

    class Meta:
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"
        ordering = ['-created_at']