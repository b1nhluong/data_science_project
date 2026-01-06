import os

# --- CONFIGURATION ---
input_folder = 'raw'
output_file = 'final_weather_merged_raw.csv'

# File order is crucial: The header from the first file will be used as the master header.
files_to_merge = ['hanoi_final.csv', 'danang_final.csv', 'HCM_final.csv']

print("--- STARTING MANUAL FILE MERGE ---")

# Open the output file for writing ('w' mode)
with open(output_file, 'w', encoding='utf-8') as outfile:
    
    for i, filename in enumerate(files_to_merge):
        file_path = os.path.join(input_folder, filename)
        
        if os.path.exists(file_path):
            print(f"-> Processing: {filename}...", end=" ")
            
            with open(file_path, 'r', encoding='utf-8') as infile:
                # Case 1: The FIRST file (i == 0)
                # We keep EVERYTHING (Header + Data)
                if i == 0:
                    data = infile.read()
                    outfile.write(data)
                    
                    # Ensure a newline exists at the end of the file content
                    if not data.endswith('\n'):
                        outfile.write('\n')
                    print("✅ Copied all content (including Header).")
                    
                # Case 2: Subsequent files (i > 0)
                # We SKIP the first line (Header) and keep the rest
                else:
                    # Read the first line (Header) but DO NOT write it
                    header = infile.readline() 
                    
                    # Read the rest of the file
                    content = infile.read()
                    
                    # Check if the file actually has data (not just a header or empty)
                    if content:
                        outfile.write(content)
                        
                        # Ensure a newline exists at the end
                        if not content.endswith('\n'):
                            outfile.write('\n')
                        print("✅ Copied data (Skipped Header).")
                    else:
                        print("⚠️ File is empty or contains only a header, skipping.")
        else:
            print(f"\n❌ File not found: {filename}")

print(f"\n--- COMPLETED: {output_file} ---")