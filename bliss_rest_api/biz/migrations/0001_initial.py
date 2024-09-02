# Generated by Django 5.1 on 2024-08-16 08:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CollectionQuery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=50, unique=True)),
                ('query', models.TextField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'bliss_collection_query',
            },
        ),
        migrations.CreateModel(
            name='FileUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tmp_file_name', models.CharField(max_length=150)),
                ('orig_file_name', models.CharField(max_length=100)),
                ('storage_file_name', models.CharField(max_length=150, null=True)),
                ('source_field', models.CharField(max_length=100, null=True)),
                ('uploaded_by', models.CharField(max_length=60)),
                ('is_moved', models.BooleanField(null=True)),
                ('moved_at', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'bliss_file_upload',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=150)),
                ('product_image', models.CharField(max_length=150)),
                ('quantity', models.IntegerField()),
                ('original_price', models.FloatField()),
                ('selling_price', models.FloatField()),
                ('description', models.TextField(max_length=150)),
                ('status', models.BooleanField(default=False)),
                ('trending', models.BooleanField(default=False)),
                ('availability', models.BooleanField(default=True)),
                ('created_by', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'bliss_product_details',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(db_index=True, max_length=255, unique=True)),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True)),
                ('user_profile', models.CharField(max_length=100, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('gender', models.CharField(max_length=100, null=True)),
                ('first_name', models.CharField(max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100, null=True)),
                ('mobile', models.CharField(max_length=15, null=True)),
                ('user_type', models.CharField(max_length=25, null=True)),
                ('address', models.CharField(max_length=500, null=True)),
                ('wrong_pwd_counts', models.IntegerField(null=True)),
                ('email_verified', models.BooleanField(default=False)),
                ('last_pwd_changed_at', models.DateTimeField(blank=True, null=True)),
                ('validate_token', models.CharField(blank=True, max_length=20, null=True)),
                ('validated_at', models.DateTimeField(blank=True, null=True)),
                ('deact_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('joining_date', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CustomerDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(db_index=True, max_length=50)),
                ('email', models.EmailField(db_index=True, max_length=150, unique=True)),
                ('mobile_number', models.CharField(db_index=True, max_length=10)),
                ('address', models.CharField(max_length=200, null=True)),
                ('city', models.CharField(max_length=150, null=True)),
                ('state', models.CharField(max_length=150, null=True)),
                ('country', models.CharField(max_length=150, null=True)),
                ('pincode', models.CharField(max_length=150, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'bliss_customer_details',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=150)),
                ('phone', models.CharField(max_length=20)),
                ('address', models.TextField()),
                ('city', models.CharField(max_length=150)),
                ('state', models.CharField(max_length=150)),
                ('country', models.CharField(max_length=150)),
                ('pincode', models.CharField(max_length=150)),
                ('total_price', models.FloatField(null=True)),
                ('payment_mode', models.CharField(max_length=150)),
                ('payment_id', models.CharField(max_length=250, null=True)),
                ('status', models.CharField(default='Pending', max_length=150)),
                ('tracking_no', models.CharField(max_length=250, null=True)),
                ('created_by', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(max_length=50)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='biz.customerdetails')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='biz.product')),
            ],
            options={
                'db_table': 'bliss_order_details',
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_qty', models.IntegerField()),
                ('created_by', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(max_length=50)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='biz.customerdetails')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='biz.product')),
            ],
            options={
                'db_table': 'bliss_cart_details',
            },
        ),
    ]
