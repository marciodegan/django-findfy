from django.shortcuts import render
from django.http import HttpResponse
from .forms import FileModelForm
from .models import File
import csv
from restaurantes.models import GoogleImport

def upload_file_view(request):
    form = FileModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        form = FileModelForm()
        obj = File.objects.get(activated=False)
        with open(obj.file_name.path, 'r') as f:
            reader = csv.reader(f)

            for i, row in enumerate(reader):
                if i==0:
                    pass
                else:                                                       
                    GoogleImport.objects.create(
                        name = row[0],
                        address = row[1],
                        place_id = row[2],
                        phone = row[3],
                        types = row[4],
                        website = row[5],
                        hours = row[6],
                    )
                    # print(row[0] "JA CADASTRADO")
                    # print(type(row))
            obj.activated = True
            obj.save()
    return render(request, 'files/upload.html', {'form': form})