# Generated by Django 4.2 on 2023-04-30 06:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payapp', '0002_rename_transactions_transaction'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='Message',
            new_name='message',
        ),
    ]
