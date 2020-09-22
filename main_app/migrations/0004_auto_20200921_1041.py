# Generated by Django 3.1 on 2020-09-21 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_auto_20200921_0858'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShoeLace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('color', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterModelOptions(
            name='purchase',
            options={'ordering': ['-date']},
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateField(verbose_name='purchase date'),
        ),
        migrations.AddField(
            model_name='sneaker',
            name='laces',
            field=models.ManyToManyField(to='main_app.ShoeLace'),
        ),
    ]
