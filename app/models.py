from django.db import models
from django.conf import settings


class CPU(models.Model):
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    cores = models.PositiveIntegerField(null=True)
    tdp = models.PositiveIntegerField(null=True)
    integrated_graphics = models.CharField(max_length=255, null=True)
    multithreading = models.BooleanField(null=True)

class GPU(models.Model):
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    chipset = models.CharField(max_length=255, null=True)
    color = models.CharField(max_length=255, null=True)
    length = models.FloatField(null=True)

class Memory(models.Model):
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    module_type = models.CharField(max_length=255, null=True)
    number_of_modules = models.PositiveIntegerField(null=True)
    color = models.CharField(max_length=255, null=True)
    first_word_latency = models.FloatField(null=True)
    cas_timing = models.PositiveIntegerField(null=True)
    error_correction = models.CharField(max_length=255, null=True)

class CPUCooler(models.Model):
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    color = models.CharField(max_length=255, null=True)
    radiator_size = models.PositiveIntegerField(null=True)

class Motherboard(models.Model):
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    socket = models.CharField(max_length=255, null=True)
    form_factor = models.CharField(max_length=255, null=True)
    ram_slots = models.PositiveIntegerField(null=True)
    color = models.CharField(max_length=255, null=True)

class StorageDrive(models.Model):
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    storage_type = models.CharField(max_length=255, null=True)
    platter_rpm = models.PositiveIntegerField(null=True)
    form_factor = models.CharField(max_length=255, null=True)
    interface = models.CharField(max_length=255, null=True)

class PSU(models.Model):
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    form_factor = models.CharField(max_length=255, null=True)
    efficiency_rating = models.CharField(max_length=255, null=True)
    wattage = models.PositiveIntegerField(null=True)
    modular = models.CharField(max_length=255, null=True)
    color = models.CharField(max_length=255, null=True)

class Case(models.Model):
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    form_factor = models.CharField(max_length=255, null=True)
    color = models.CharField(max_length=255, null=True)
    psu_wattage = models.PositiveIntegerField(null=True)
    side_panel = models.BooleanField(null=True)
    external_bays = models.PositiveIntegerField(null=True)
    internal_bays = models.PositiveIntegerField(null=True)

class CaseFans(models.Model):
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    size = models.PositiveIntegerField(null=True)
    color = models.CharField(max_length=255, null=True)
    pwm = models.BooleanField(null=True)

class Computer(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="computers",
    )
    cpu = models.ForeignKey(CPU, models.SET_NULL, null=True)
    motherboard = models.ForeignKey(Motherboard, models.SET_NULL, null=True)
    gpu = models.ForeignKey(GPU, models.SET_NULL, null=True)
    memory = models.ForeignKey(Memory, models.SET_NULL, null=True)
    storagedrive = models.ForeignKey(StorageDrive, models.SET_NULL, null=True)
    cpucooler = models.ForeignKey(CPUCooler, models.SET_NULL, null=True)
    psu = models.ForeignKey(PSU, models.SET_NULL, null=True)
    case = models.ForeignKey(Case, models.SET_NULL, null=True)
    fan = models.ForeignKey(CaseFans, models.SET_NULL, null=True)


class Conversation(models.Model):
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="conversations"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=100)

    @property
    def is_private(self):
        return self.participants.count() == 2


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_messages"
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

