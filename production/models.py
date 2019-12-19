from django.db import models

# Create your models here.
class Member(models.Model):
    MemberID = models.PositiveIntegerField(primary_key = True)
    mName = models.CharField(max_length = 20)
    Gender = models.CharField(max_length = 10)
    Phone = models.CharField(max_length = 13)
    Email = models.EmailField(max_length = 100, blank = True)
    BDay = models.DateField(null = False)
    Pets = models.BooleanField
    Student = models.BooleanField

class Dish(models.Model):
    dName = models.CharField(max_length = 50, primary_key = True)
    dPrice = models.PositiveIntegerField()

class Stock(models.Model):
    sName = models.CharField(max_length = 50, primary_key = True)
    sNum = models.PositiveIntegerField()
    sPrice = models.PositiveIntegerField()
    Expierd = models.DateField()

class Equipment(models.Model):
    eName = models.CharField(max_length = 50, primary_key = True)
    eNum = models.PositiveIntegerField()
    ePrice = models.PositiveIntegerField()

class Firm(models.Model):
    FirmID = models.PositiveIntegerField(primary_key = True)
    fName = models.CharField(max_length = 20)
    Tele = models.CharField(max_length = 10)
    Address = models.CharField(max_length = 50)

class Order(models.Model):
    oTime = models.DateTimeField(auto_now_add = 'True')
    MemberID = models.ForeignKey(Member, on_delete=models.CASCADE)
    dName = models.ForeignKey(Dish, on_delete=models.CASCADE)
    oNum = models.PositiveIntegerField()
    class Meta: 
     unique_together = (("oTime","MemberID", "dName"))

class Made(models.Model):
    mTime = models.DateTimeField(auto_now_add = 'True')
    mDish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    mStock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    mNum = models.PositiveIntegerField()
    class Meta: 
     unique_together = (("mTime","mDish", "mStock")) 

class ProvideStock(models.Model):
    psTime = models.DateTimeField(auto_now_add = 'True', primary_key = True)
    psFirm = models.ForeignKey(Firm, on_delete=models.CASCADE)
    pStock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    psNum = models.PositiveIntegerField()
    class Meta: 
     unique_together = (("psTime","pStock", "psNum")) 

class ProvideEquip(models.Model):
    peTime = models.DateTimeField(auto_now_add = 'True', primary_key = True)
    peFirm = models.ForeignKey(Firm, on_delete=models.CASCADE)
    pEquip = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    peNum = models.PositiveIntegerField()
    class Meta: 
     unique_together = (("peTime","pEquip", "peNum"))
