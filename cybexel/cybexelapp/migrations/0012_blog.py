# Generated by Django 5.2.3 on 2025-07-07 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cybexelapp', '0011_jobapplication'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('heading', models.CharField(max_length=200)),
                ('content', models.TextField(help_text='Separate paragraphs with `||`')),
                ('image', models.ImageField(upload_to='blogs/')),
            ],
        ),
    ]
