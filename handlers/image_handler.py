def image_handler():
    import os
    import tkinter as tk
    from tkinter import filedialog
    from PIL import Image, ExifTags
    from PIL.ExifTags import GPSTAGS
    import subprocess
    import json

    def extract_all_metadata(image_path):
        result = subprocess.run(
            ['exiftool', '-j', '-a', '-u', '-g1', image_path],
            stdout=subprocess.PIPE
        )
        metadata = json.loads(result.stdout)[0]
        return metadata

    # Create hidden root window
    root = tk.Tk()
    root.withdraw()
    
    # Configure file dialog
    supported_extensions = (
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif",
        ".webp", ".raw", ".heif", ".heic", ".dng", ".cr2", ".nef"
    )
    file_types = [("Image Files", " ".join(f"*{ext}" for ext in supported_extensions))]

    # Show file selection dialog
    image_path = filedialog.askopenfilename(
        title="Select Image File",
        filetypes=file_types
    )

    # Exit if user cancels selection
    if not image_path:
        print("No file selected.")
        return

    # Original file validation logic
    if not (os.path.isfile(image_path) and image_path.lower().endswith(supported_extensions)):
        print("Invalid image path or unsupported file type.")
        return

    # Rest of the original code remains unchanged...
    try:
        with Image.open(image_path) as img:
            # Get EXIF data with enhanced compatibility
            exif_data = {}
            try:
                exif_data = img._getexif() or {}
            except Exception:
                try:
                    exif_data = img.getexif() or {}
                except Exception:
                    pass

            if not exif_data:
                print("No standard EXIF data found in image")
            else:
                print("\n=== EXIF DATA ===")
                for tag_id, value in exif_data.items():
                    tag_name = ExifTags.TAGS.get(tag_id, tag_id)
                    print(f"{tag_name}: {value}")

                # Geolocation extraction functions
                def get_geolocation(exif):
                    gps_info = {}
                    if 34853 in exif:
                        for key in exif[34853].keys():
                            decoded = GPSTAGS.get(key, key)
                            gps_info[decoded] = exif[34853][key]
                    return gps_info

                def dms_to_decimal(dms, ref):
                    try:
                        degrees = dms[0][0] / dms[0][1]
                        minutes = dms[1][0] / dms[1][1] / 60
                        seconds = dms[2][0] / dms[2][1] / 3600
                        decimal = degrees + minutes + seconds
                        return -decimal if ref in ('S', 'W') else decimal
                    except:
                        return None

                gps_data = get_geolocation(exif_data)
                if gps_data:
                    print("\n=== GEOLOCATION ===")
                    lat = dms_to_decimal(
                        gps_data.get('GPSLatitude', []),
                        gps_data.get('GPSLatitudeRef', 'N')
                    )
                    lon = dms_to_decimal(
                        gps_data.get('GPSLongitude', []),
                        gps_data.get('GPSLongitudeRef', 'E')
                    )
                    
                    if lat and lon:
                        print(f"Latitude: {lat:.6f}")
                        print(f"Longitude: {lon:.6f}")
                        print(f"Google Maps: https://www.google.com/maps?q={lat},{lon}")
                    else:
                        print("Geolocation data incomplete or corrupted")
                    
                    for key, value in gps_data.items():
                        print(f"{key}: {value}")
                else:
                    print("\nNo geolocation data found in EXIF")

                # Date/time extraction with better formatting
                print("\n=== DATE/TIME ===")
                datetime_tags = {
                    306: 'DateTime',
                    36867: 'DateTimeOriginal',
                    36868: 'DateTimeDigitized'
                }
                
                captured_time = None
                for tag_id, tag_name in datetime_tags.items():
                    if tag_id in exif_data:
                        captured_time = exif_data[tag_id]
                        try:
                            # Improved datetime formatting
                            formatted_time = captured_time.replace(':', '-', 2).replace(' ', 'T', 1)
                            print(f"{tag_name}: {formatted_time}")
                        except AttributeError:
                            print(f"{tag_name}: {captured_time}")
                        break
                else:
                    print("No date/time information found")

            # Integrated XMP metadata check
            try:
                with open(image_path, 'rb') as f:
                    content = f.read().decode('latin-1')
                    xmp_start = content.find('<x:xmpmeta')
                    xmp_end = content.find('</x:xmpmeta>')
                    if xmp_start != -1 and xmp_end != -1:
                        xmp_data = content[xmp_start:xmp_end+12]
                        print("\n=== XMP METADATA ===")
                        print(xmp_data)
                    else:
                        print("\nNo XMP metadata found")
            except Exception as e:
                print(f"\nXMP Metadata Error: {str(e)}")

    except Exception as e:
        print(f"\nERROR: {str(e)}")
        if "cannot identify image file" in str(e):
            print("The file might be corrupted or not a supported image format")
        elif "truncated" in str(e):
            print("The image file appears to be truncated")
        elif "Permission denied" in str(e):
            print("Permission denied - check file access rights")

# Entry point
if __name__ == "__main__":
    image_handler()