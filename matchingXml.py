import os
import pydicom
import shutil

def get_dicom_instance_ids(directory_path):
    dicom_instances = {}

    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.dcm'):
                file_path = os.path.join(root, file)
                try:
                    dcm_data = pydicom.dcmread(file_path)
                    instance_id = dcm_data.SOPInstanceUID
                    dicom_instances[file_path] = instance_id
                except pydicom.errors.InvalidDicomError:
                    print(f"Invalid DICOM file: {file_path}")
                except Exception as e:
                    print(f"Error processing {file_path}: {str(e)}")

    return dicom_instances

def find_matching_xml_files(result_dict, xml_directory_path):
    xml_matches = {}

    for dicom_filename, instance_id in result_dict.items():
        # Extract the ID from the dicom filename
        id_part = dicom_filename.split(os.sep)[1]
        id_part = id_part.split('-')[1] 
        
        # Construct the path to the corresponding Annotation folder
        annotation_folder_path = os.path.join(xml_directory_path, id_part)
        
        if os.path.isdir(annotation_folder_path):
            for xml_file in os.listdir(annotation_folder_path):
                if xml_file.endswith('.xml'):
                    xml_file_path = os.path.join(annotation_folder_path, xml_file)
                    xml_filename = os.path.splitext(xml_file)[0]

                    if instance_id == xml_filename:
                        xml_matches[dicom_filename] = xml_file_path
                        break

    return xml_matches

if __name__ == "__main__":
    directory_path = 'patient_data-1'
    xml_directory_path = 'Annotation'
    target_dicom_folder = 'matched_dicom'
    target_xml_folder = 'matched_xml'

    result_dict = get_dicom_instance_ids(directory_path)
    matching_xml_files = find_matching_xml_files(result_dict, xml_directory_path)

    # Create the target folders if they don't exist
    if not os.path.exists(target_dicom_folder):
        os.makedirs(target_dicom_folder)
    if not os.path.exists(target_xml_folder):
        os.makedirs(target_xml_folder)

    id_part_count = {}  # To keep track of the count for each id_part
    for dicom_filename, xml_file_path in matching_xml_files.items():
        # Extract the ID from the dicom filename
        id_part = dicom_filename.split(os.sep)[1]
        id_part = id_part.split('-')[1][0]  # Extract the first character (A or B)

        # Increment the count for the current id_part
        id_part_count[id_part] = id_part_count.get(id_part, 0) + 1

        # Construct the path for the target DICOM file and XML file
        target_dicom_file_path = os.path.join(target_dicom_folder, f"{id_part}{id_part_count[id_part]:04d}.dcm")
        target_xml_file_path = os.path.join(target_xml_folder, f"{id_part}{id_part_count[id_part]:04d}.xml")

        # Copy the DICOM file and the corresponding annotation file to the target folders with the new filenames
        shutil.copy(dicom_filename, target_dicom_file_path)
        shutil.copy(xml_file_path, target_xml_file_path)

    print("DICOM and XML files saved in separate folders.")

    # print(matching_xml_files)










# # import pydicom

# # # Reading a DICOM file from a specific path
# # dcm_data = pydicom.dcmread('manifest-1608669183333\\Lung-PET-CT-Dx\\Lung_Dx-A0001\\04-04-2007-NA-Chest-07990\\2.000000-5mm-40805\\1-14.dcm')
# # print(dcm_data.SOPInstanceUID)

# # import os
# # import pydicom

# # def get_dicom_instance_ids(directory_path):
# #     dicom_instances = {}

# #     for root, _, files in os.walk(directory_path):
# #         for file in files:
            
# #             if file.endswith('.dcm'):
# #                 file_path = os.path.join(root, file)
# #                 # print(file_path)
# #                 try:
# #                     dcm_data = pydicom.dcmread(file_path)
# #                     instance_id = dcm_data.SOPInstanceUID
# #                     dicom_instances[file_path] = instance_id
# #                 except pydicom.errors.InvalidDicomError:
# #                     print(f"Invalid DICOM file: {file_path}")
# #                 except Exception as e:
# #                     print(f"Error processing {file_path}: {str(e)}")

# #     return dicom_instances

# # # Replace 'path_to_directory' with the actual path to your directory containing DCM files
# # directory_path = 'patient_data-1'
# # result_dict = get_dicom_instance_ids(directory_path)

# # # # Printing the resulting dictionary
# # # for filename, instance_id in result_dict.items():
# # #     print(f"File: {filename}, Instance ID: {instance_id}")


# # def find_matching_xml_files(result_dict, xml_directory_path):
# #     xml_matches = {}

# #     for dicom_filename, instance_id in result_dict.items():
# #         for root, _, files in os.walk(xml_directory_path):
# #             for xml_file in files:
# #                 if xml_file.endswith('.xml'):
# #                     xml_file_path = os.path.join(root, xml_file)
# #                     xml_filename = os.path.splitext(xml_file)[0]

# #                     if instance_id == xml_filename:
# #                         xml_matches[dicom_filename] = xml_file_path
# #                         break

# #     return xml_matches

# # xml_directory_path = 'manifest-1608669183333\\A0001'
# # matching_xml_files = find_matching_xml_files(result_dict, xml_directory_path)
# # print(len(matching_xml_files))

# # Printing the resulting dictionary
# # for dicom_filename, xml_file_path in matching_xml_files.items():
# #     print(f"DICOM File: {dicom_filename}, Matching XML File: {xml_file_path}")

