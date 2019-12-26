from django.db import models


# Create your models here.
class Member(models.Model):
    MemberID = models.PositiveIntegerField(primary_key=True)
    mName = models.CharField(max_length=20)
    Gender = models.CharField(max_length=10)
    Phone = models.CharField(max_length=13)
    Email = models.EmailField(max_length=100, blank=True)
    BDay = models.DateField(null=False)
    Pets = models.BooleanField(default=True)
    Student = models.BooleanField(default=True)

    def __str__(self):
        result = str(self.MemberID) + ' ' + str(self.mName)
        return result


class Dish(models.Model):
    dName = models.CharField(max_length=50, primary_key=True)
    dPrice = models.PositiveIntegerField()
    Mid = models.ManyToManyField(Member, through='Order')

    def __str__(self):
        return self.dName


class Firm(models.Model):
    FirmID = models.PositiveIntegerField(primary_key=True)
    fName = models.CharField(max_length=20)
    Tele = models.CharField(max_length=10)
    Address = models.CharField(max_length=50)

    def __str__(self):
        result = str(self.FirmID) + ' ' + str(self.fName)
        return result

class Stock(models.Model):
    sName = models.CharField(max_length=50, primary_key=True)
    sNum = models.PositiveIntegerField()
    Expired = models.DateField()
    dish = models.ManyToManyField(Dish, through='Made')
    firm = models.ManyToManyField(Firm, through='ProvideStock')

    class Meta:
        unique_together = ('sName', 'Expired')

    def __str__(self):
        result = str(self.sName) + ' ' + str(self.sNum) + ' ' + str(self.Expired)
        return result


class Equipment(models.Model):
    eName = models.CharField(max_length=50, primary_key=True)
    eNum = models.PositiveIntegerField()
    firm = models.ManyToManyField(Firm, through='ProvideEquip')

    def __str__(self):
        result = str(self.eName) + ' ' + str(self.eNum)
        return result


class Order(models.Model):
    oTime = models.DateTimeField(auto_now_add='True', primary_key=True)
    MID = models.ForeignKey(Member, on_delete=models.CASCADE)
    dishName = models.ForeignKey(Dish, on_delete=models.CASCADE)
    orderNum = models.PositiveIntegerField()

    class Meta:
        unique_together = ("oTime", "MID", "dishName")
    def __str__(self):
        result = str(self.oTime) + ' ' + str(self.MID) + ' ' + str(self.dishName) + ' ' + str(self.orderNum)
        return result

class Made(models.Model):
    mTime = models.DateTimeField(auto_now_add='True', primary_key=True)
    mDish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    mStock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    mNum = models.PositiveIntegerField()

    class Meta:
        unique_together = ("mTime", "mDish", "mStock")

    def __str__(self):
        result = str(self.mTime) + ' ' + str(self.mDish) + ' ' + str(self.mStock) + ' ' + str(self.mNum)
        return result


class ProvideStock(models.Model):
    psTime = models.DateTimeField(auto_now_add='True', primary_key=True)
    psFirm = models.ForeignKey(Firm, on_delete=models.CASCADE)
    pStock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    psNum = models.PositiveIntegerField()

    class Meta:
        unique_together = ("psTime", "pStock", "psNum")
    def __str__(self):
        result = str(self.psTime) + ' ' + str(self.psFirm) + ' ' + str(self.pStock) + ' ' + str(self.psNum)
        return result

class ProvideEquip(models.Model):
    peTime = models.DateTimeField(auto_now_add='True', primary_key=True)
    peFirm = models.ForeignKey(Firm, on_delete=models.CASCADE)
    pEquip = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    peNum = models.PositiveIntegerField()

    class Meta:
        unique_together = ("peTime", "pEquip", "peNum")

    def __str__(self):
        result = str(self.peTime) + ' ' + str(self.peNum) + ' ' + str(self.pEquip) + ' ' + str(self.peNum)
        return result
