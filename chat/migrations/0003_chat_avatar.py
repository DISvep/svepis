# Generated by Django 5.1.4 on 2025-02-03 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_chat_privatechat_alter_message_room_delete_chatroom'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='chat/avatar/'),
        ),
    ]
