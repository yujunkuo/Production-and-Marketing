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


class Inventory(models.Model):
    invID = models.PositiveIntegerField(primary_key=True)
    invName = models.CharField(max_length=50)
    invNum = models.PositiveIntegerField()
    Expired = models.DateField()
    dish = models.ManyToManyField(Dish, through='Made')
    firm = models.ManyToManyField(Firm, through='ProvideInventory')

    def __str__(self):
        result = str(self.invName) + ' ' + str(self.invNum) + ' ' + str(self.Expired)
        return result


class Equipment(models.Model):
    eName = models.CharField(max_length=50, primary_key=True)
    eNum = models.PositiveIntegerField()
    firm = models.ManyToManyField(Firm, through='ProvideEquip')

    def __str__(self):
        result = str(self.eName) + ' ' + str(self.eNum)
        return result


class Order(models.Model):
    oID = models.PositiveIntegerField(primary_key=True)
    oTime = models.DateTimeField()
    MID = models.ForeignKey(Member, on_delete=models.CASCADE)
    dishName = models.ForeignKey(Dish, on_delete=models.CASCADE)
    orderNum = models.PositiveIntegerField()

    def __str__(self):
        result = str(self.oTime) + ' ' + str(self.MID) + ' ' + str(self.dishName) + ' ' + str(self.orderNum)
        return result


class Made(models.Model):
    madeID = models.PositiveIntegerField(primary_key=True)
    mTime = models.DateTimeField(auto_now_add=True)
    mDish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    mInvent = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    mNum = models.PositiveIntegerField()

    def __str__(self):
        result = str(self.mTime) + ' ' + str(self.mDish) + ' ' + str(self.mInvent) + ' ' + str(self.mNum)
        return result


class ProvideInventory(models.Model):
    piTime = models.DateTimeField(auto_now_add='True', primary_key=True)
    piFirm = models.ForeignKey(Firm, on_delete=models.CASCADE)
    pInvent = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    piNum = models.PositiveIntegerField()

    def __str__(self):
        result = str(self.piTime) + ' ' + str(self.piNum)
        return result


class ProvideEquip(models.Model):
    peTime = models.DateTimeField(auto_now_add='True', primary_key=True)
    peFirm = models.ForeignKey(Firm, on_delete=models.CASCADE)
    pEquip = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    peNum = models.PositiveIntegerField()

    def __str__(self):
        result = str(self.peTime) + ' ' + str(self.pEquip) + ' ' + str(self.peNum)
        return result
