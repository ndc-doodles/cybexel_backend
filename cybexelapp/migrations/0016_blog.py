# Generated by Django 5.2.3 on 2025-07-07 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cybexelapp', '0015_delete_blog'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('short_heading', models.CharField(help_text='Heading for card display', max_length=150)),
                ('full_heading', models.CharField(help_text='Full heading for modal display', max_length=250)),
                ('paragraph1', models.TextField()),
                ('paragraph2', models.TextField(blank=True, null=True)),
                ('paragraph3', models.TextField(blank=True, null=True)),
                ('paragraph4', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(upload_to='blogs/')),
            ],
        ),
    ]
