# Generated by Django 3.0.8 on 2022-05-13 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='basiccontact',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=50)),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Emaildataofuser',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('subject', models.CharField(max_length=50)),
                ('message', models.CharField(max_length=50)),
                ('rollno', models.CharField(max_length=50)),
                ('profname', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Emailverify',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=50)),
                ('otp', models.CharField(max_length=6)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Passwordreset',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254)),
                ('otp', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Recorduserentry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=64)),
                ('ip', models.GenericIPAddressField(null=True)),
                ('username', models.CharField(max_length=256, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='teacherimage',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='teachers/questions')),
            ],
        ),
    ]