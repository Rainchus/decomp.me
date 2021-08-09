import os
import uuid

from django.conf import settings
from django.db import models

# TODO: These are only kept around for the migrations that depend on them
# They can be removed once the migrations are squashed
def asm_objects_path():
    return settings.BASE_DIR / "local_files" / "assemblies"

def compilation_objects_path():
    return settings.BASE_DIR / "local_files" / "compilations"

class Profile(models.Model):
    pass

class Compiler(models.Model):
    shortname = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    assemble_cmd = models.CharField(max_length=1000)
    compile_cmd = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

class CompilerConfiguration(models.Model):
    compiler = models.ForeignKey(Compiler, on_delete=models.CASCADE)
    as_flags = models.CharField(max_length=100)
    cc_flags = models.CharField(max_length=100)

    def __str__(self):
        return self.compiler.name + " " + self.cc_flags

class Asm(models.Model):
    hash = models.CharField(max_length=64, primary_key=True)
    data = models.TextField()

    def __str__(self):
        return self.data

class Assembly(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    compiler_config = models.ForeignKey(CompilerConfiguration, on_delete=models.CASCADE)
    source_asm = models.ForeignKey(Asm, on_delete=models.CASCADE)
    elf_object = models.BinaryField(blank=True)

class Compilation(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    compiler_config = models.ForeignKey(CompilerConfiguration, on_delete=models.CASCADE)
    source_code = models.TextField()
    context = models.TextField(blank=True)
    elf_object = models.BinaryField(blank=True)

class Scratch(models.Model):
    slug = models.SlugField(primary_key=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    compiler_config = models.ForeignKey(CompilerConfiguration, on_delete=models.CASCADE)
    target_assembly = models.ForeignKey(Assembly, on_delete=models.CASCADE)
    source_code = models.TextField(blank=True)
    context = models.TextField(blank=True)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.slug
