# Generated by Django 4.2 on 2024-12-07 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('recipient_email', models.EmailField(max_length=254)),
                ('envelope_id', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(default='created', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('document', models.FileField(upload_to='contracts/')),
            ],
        ),
    ]
