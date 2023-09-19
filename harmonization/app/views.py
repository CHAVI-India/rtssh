
import os
import json
import shutil
import zipfile
from django.conf import settings
from django.shortcuts import render, redirect
from .models import UploadedFile, ProcessedFile
from .preprocess.harmonization import harmonization
from django.core.files.storage import FileSystemStorage
# from .TG263data import tg263_data_upload



def index_view(request):
    return render(request, "index.html")

def docs_view(request):
    return render(request, "docs-page.html")


def upload_view(request):
    # Upload TG263 data
    # from app.preprocess.TG263data import TG263_data
    # TG263_data()

    if request.method == 'POST' and request.FILES.get('zip_file'):
        zip_file = request.FILES['zip_file']
        
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'uploads'))
        uploaded_file = fs.save(zip_file.name, zip_file)
        uploaded_file_obj = UploadedFile.objects.create(file=uploaded_file)

        return redirect('preprocess')    
    return render(request, 'upload.html', {"page_title": "CLH | Upload"})


def preprocess_view(request):
    if request.method == 'POST' and request.POST.get('selected_file'):
        selected_file_id = request.POST.get('selected_file')
        try:
            uploaded_file = UploadedFile.objects.get(id=selected_file_id)
        except UploadedFile.DoesNotExist:
            error_message = "Selected file does not exist."
            return render(request, 'preprocess.html', {'error_message': error_message})

        zip_path = os.path.join(settings.MEDIA_ROOT, 'uploads', uploaded_file.file.name)
        temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
        temp_unzip_dir = os.path.join(temp_dir, 'temp_unzipped')

        preprocess_info = {
            "type": "Preprocess Info",
            "Selected File ID": selected_file_id,
            "Zip Path": zip_path
        }

        try:
            # Ensure the "downloads" folder exists, create it if not
            download_folder = os.path.join(settings.MEDIA_ROOT, 'downloads')
            os.makedirs(download_folder, exist_ok=True)

            # Extract the selected ZIP file to a temporary directory
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_unzip_dir)
                

            # Perform harmonization on the files in the temporary directory
            # Replace this with your actual harmonization logic

            def check_and_operate_on_subfolders(path):
                if any(os.path.isdir(os.path.join(path, item)) for item in os.listdir(path)):
                    # print(f"The folder at '{path}' contains subfolders.")
                    harmonization(main_path=temp_unzip_dir)
                    preprocess_info["Harmonization File type"] = "Multiple Subfolders"
                    # Perform your desired operation here for the subfolders
                else:
                    # print(f"The folder at '{path}' does not contain subfolders.")
                    harmonization(main_path=temp_dir)
                    preprocess_info["Harmonization File type"] = "Single folders"

            # Example usage:
            folder_path = temp_unzip_dir
            check_and_operate_on_subfolders(folder_path)
            
            # Get the base name of the selected input ZIP file
            base_name = os.path.splitext(os.path.basename(uploaded_file.file.name))[0]
            processed_zip_filename = f'{base_name}_processed.zip'
        
            # Specify the directory where you want to save the processed file
            processed_directory = os.path.join(settings.MEDIA_ROOT, 'downloads')
            processed_zip_path = os.path.join(processed_directory, processed_zip_filename)

            preprocess_info["Processed Zip Filename"] = processed_zip_filename
            preprocess_info["Processed Zip Filepath"] = processed_zip_path

            with zipfile.ZipFile(processed_zip_path, 'w') as zipf:
                for root, dirs, files in os.walk(temp_unzip_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, temp_unzip_dir)
                        zipf.write(file_path, arcname)

            # Clean up the temporary unzipped folder
            shutil.rmtree(temp_unzip_dir, ignore_errors=True)

            # Create a ProcessedFile entry for the processed file
            processed_file = ProcessedFile(file=processed_zip_path)
            processed_file.save()

            # Preporocess information
            preprocess_info_json = json.dumps(preprocess_info, indent=4)
            print(preprocess_info_json)
            # Redirect to the download page after preprocessing
            return redirect('download', processed_file_id=processed_file.id)


        except Exception as e:
            
            # Clean up the temporary unzipped folder on error
            shutil.rmtree(temp_unzip_dir, ignore_errors=True)
            error_message = "An error occurred during preprocessing. Please rezip and try again."
            return render(request, 'preprocess.html', {'error_message': error_message, "page_title": "CLH | Preprocess"})

    uploaded_files = UploadedFile.objects.all()  # Retrieve all uploaded files
    return render(request, 'preprocess.html', {'uploaded_files': uploaded_files, "page_title": "CLH | Preprocess"})


def download_view(request, processed_file_id):
    processed_file = ProcessedFile.objects.get(id=processed_file_id)
    download_filename = processed_file.file.name
    download_url = processed_file.file.url

    # file name
    file_name = download_filename.split('\\')[-1]

    download_info = {
        "Type": "Download Info",
        "File ID": processed_file_id,
        "Filename" : file_name,
        "Donwload URL": download_url  
    }

    download_json_info = json.dumps(download_info, indent=4)
    print(download_json_info)
    return render(request, 'download.html', {'download_link': download_url, "download_filename": file_name, "page_title": "CLH | Download"})






 