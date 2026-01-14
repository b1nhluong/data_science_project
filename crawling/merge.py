import os

# --- CONFIGURATION ---
input_folder = 'raw'
output_file = 'final_weather_merged_raw.csv'

files_to_merge = ['hanoi_final.csv', 'danang_final.csv', 'HCM_final.csv']

print("--- STARTING MANUAL FILE MERGE ---")
with open(output_file, 'w', encoding='utf-8') as outfile:
    
    for i, filename in enumerate(files_to_merge):
        file_path = os.path.join(input_folder, filename)
        
        if os.path.exists(file_path):
            print(f"-> Processing: {filename}...", end=" ")
            
            with open(file_path, 'r', encoding='utf-8') as infile:
                if i == 0:
                    data = infile.read()
                    outfile.write(data)
                    
                    if not data.endswith('\n'):
                        outfile.write('\n')
                    print("Copied all content (including Header).")
                    
                else:
                    header = infile.readline()
                    content = infile.read()
                
                    if content:
                        outfile.write(content)
                        
                        if not content.endswith('\n'):
                            outfile.write('\n')
                        print("Copied data (Skipped Header).")
                    else:
                        print("File is empty or contains only a header, skipping.")
        else:
            print(f"\nFile not found: {filename}")

print(f"\n--- COMPLETED: {output_file} ---")
