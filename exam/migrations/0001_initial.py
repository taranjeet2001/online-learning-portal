# Generated by Django 3.0.8 on 2022-05-13 14:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Quizz',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('group', models.CharField(max_length=10)),
                ('subject', models.CharField(max_length=50)),
                ('chapter', models.CharField(max_length=50)),
                ('topic', models.CharField(max_length=100)),
                ('question', models.CharField(max_length=500)),
                ('option1', models.CharField(max_length=100)),
                ('option2', models.CharField(max_length=100)),
                ('option3', models.CharField(max_length=100)),
                ('option4', models.CharField(max_length=100)),
                ('answer', models.CharField(max_length=100)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('marks', models.IntegerField(default=1)),
                ('status', models.CharField(choices=[('draft', 'draft'), ('published', 'published')], default='draft', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Quizztopic',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('group', models.CharField(max_length=10)),
                ('subject', models.CharField(max_length=50)),
                ('chapter', models.CharField(max_length=50)),
                ('topic', models.CharField(max_length=100)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('date', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='studentquizzstatus',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=20)),
                ('group', models.CharField(max_length=10)),
                ('subject', models.CharField(max_length=50)),
                ('chapter', models.CharField(max_length=50)),
                ('topic', models.CharField(max_length=100)),
                ('marks', models.IntegerField()),
                ('totalmarks', models.IntegerField()),
                ('status', models.CharField(choices=[('disabled', 'done'), ('pending', 'pending')], default='pending', max_length=20)),
            ],
        ),
    ]