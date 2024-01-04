# Generated by Django 4.2.4 on 2023-12-07 21:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('due_date', models.DateField()),
                ('status', models.CharField(choices=[('Incomplete', 'Incomplete'), ('Complete', 'Complete')], default='Incomplete', max_length=20)),
                ('importance', models.CharField(choices=[('most_important', 'Most Important'), ('very_important', 'Very Important'), ('important', 'Important'), ('not_important', 'Not Important')], default='not_important', max_length=20)),
                ('is_deleted', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
