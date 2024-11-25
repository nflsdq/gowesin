# Generated by Django 5.1.2 on 2024-11-10 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0007_alter_sepeda_id_sepeda_alter_sepeda_jenis_sepeda_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sepeda',
            name='id_sepeda',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='sepeda',
            name='jenis_sepeda',
            field=models.CharField(choices=[('SG', 'Sepeda Gunung'), ('SE', 'Sepeda Elektrik'), ('SA', 'Sepeda Anak'), ('S', 'Skuter')], max_length=50),
        ),
        migrations.AlterField(
            model_name='sepeda',
            name='kondisi_sepeda',
            field=models.CharField(choices=[('R', 'Rusak'), ('B', 'Baik')], max_length=50),
        ),
        migrations.AlterField(
            model_name='sepeda',
            name='status_sepeda',
            field=models.CharField(choices=[('T', 'Tersedia'), ('TT', 'Tidak Tersedia'), ('D', 'Dipinjam')], max_length=20),
        ),
    ]
