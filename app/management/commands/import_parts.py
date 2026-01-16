from django.core.management.base import BaseCommand
from app.models import *
from pcpartpicker import API


class Command(BaseCommand):
    help = "Import PC parts from PCPartPicker"

    def handle(self, *args, **kwargs):
        api = API()

        cpu_data = api.retrieve("cpu")
        cpu_list = cpu_data["cpu"]
        for item in cpu_list:
            CPU.objects.create(
                brand=item.brand,
                model=item.model,
                cores=item.cores,
                tdp=item.tdp,
                integrated_graphics=item.integrated_graphics,
                multithreading=item.multithreading,
            )

        gpu_data = api.retrieve("video-card")
        gpu_list = gpu_data["video-card"]
        for item in gpu_list:
            GPU.objects.create(
                brand=item.brand,
                model=item.model,
                chipset=item.chipset,
                color=item.color,
                length=item.length,
            )

        CPUCooler_data = api.retrieve("cpu-cooler")
        CPUCooler_list = CPUCooler_data["cpu-cooler"]
        for item in CPUCooler_list:
            CPUCooler.objects.create(
                brand=item.brand,
                model=item.model,
                color=item.color,
                radiator_size=item.radiator_size,
            )

        motherboard_data = api.retrieve("motherboard")
        motherboard_list = motherboard_data["motherboard"]
        for item in motherboard_list:
            Motherboard.objects.create(
                brand=item.brand,
                model=item.model,
                socket=item.socket,
                form_factor=item.form_factor,
                ram_slots=item.ram_slots,
                color=item.color,
            )

        Memory_data = api.retrieve("memory")
        Memory_list = Memory_data["memory"]
        for item in Memory_list:
            Memory.objects.create(
                brand=item.brand,
                model=item.model,
                module_type=item.module_type,
                number_of_modules=item.number_of_modules,
                color=item.color,
                first_word_latency=item.first_word_latency,
                cas_timing=item.cas_timing,
                error_correction=item.error_correction,
            )

        StorageDrive_data = api.retrieve("internal-hard-drive")
        StorageDrive_list = StorageDrive_data["internal-hard-drive"]
        for item in StorageDrive_list:
            StorageDrive.objects.create(
                brand=item.brand,
                model=item.model,
                storage_type=item.storage_type,
                platter_rpm=item.platter_rpm,
                form_factor=item.form_factor,
                interface=item.interface,
            )

        psu_data = api.retrieve("power-supply")
        psu_list = psu_data["power-supply"]
        for item in psu_list:
            PSU.objects.create(
                brand=item.brand,
                model=item.model,
                form_factor=item.form_factor,
                efficiency_rating=item.efficiency_rating,
                wattage=item.wattage,
                modular=item.modular,
                color=item.color,
            )

        case_data = api.retrieve("case")
        case_list = case_data["case"]
        for item in case_list:
            Case.objects.create(
                brand=item.brand,
                model=item.model,
                form_factor=item.form_factor,
                color=item.color,
                psu_wattage=item.psu_wattage,
                side_panel=item.side_panel,
                external_bays=item.external_bays,
                internal_bays=item.internal_bays,
            )

        caseFans_data = api.retrieve("case-fan")
        caseFans_list = caseFans_data["case-fan"]
        for item in caseFans_list:
            CaseFans.objects.create(
                brand=item.brand,
                model=item.model,
                size=item.size,
                color=item.color,
                pwm=item.pwm,
            )

        self.stdout.write(self.style.SUCCESS("PC parts import complete!"))
