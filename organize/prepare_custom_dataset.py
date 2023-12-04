import os
import subprocess
import csv
import shutil

test_index = 136

audio_src_folder = '/Users/apple/Downloads/david_chappelle_processes/'
destination_folder = '/Users/apple/Desktop/Practicum/self-collect-dataset-2'
id_0 = 16
id_1 = 9
def single_speaker_to_libriTTS_format():
    # Ensure the output folder exists, or create it if it doesn't
    src_folder = audio_src_folder
    dst_folder = f"{destination_folder}/dev-clean/{id_0}/{id_1}"
    test_dst_folder = f"{destination_folder}/test-clean/{id_0}/{id_1}"
    os.makedirs(dst_folder, exist_ok=True)
    if test_index != -1: os.makedirs(test_dst_folder, exist_ok=True)

    print(f"Train [0:{test_index}]")

    transcriptions = []
    test_transcriptions = []

    # Loop through all files in the input folder
    cnt = 0
    for filename in os.listdir(src_folder):
        if filename.endswith('.aifc') or filename.endswith('.mp3'):
            input_file = os.path.join(src_folder, filename)
            file_index = os.path.splitext(filename)[0]
            if cnt >= test_index:
                output_file = os.path.join(test_dst_folder, f'{id_0}_{id_1}_{file_index}.wav')
            else:
                output_file = os.path.join(dst_folder, f'{id_0}_{id_1}_{file_index}.wav')
            # Use subprocess to run FFmpeg to convert the file
            cmd = ['ffmpeg', '-i', input_file, '-ac', '1', '-ar', '24000', output_file]
            try:
                subprocess.run(cmd, check=True)
                print(f"Converted {input_file} to {output_file}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to convert {input_file}: {e}")
            cnt += 1
        elif filename.endswith('.wav'):
            input_file = os.path.join(src_folder, filename)
            file_index = os.path.splitext(filename)[0]
            if cnt >= test_index:
                output_file = os.path.join(test_dst_folder, f'{id_0}_{id_1}_{file_index}.wav')
            else:
                output_file = os.path.join(dst_folder, f'{id_0}_{id_1}_{file_index}.wav')
            shutil.copyfile(input_file, output_file)
            cnt += 1
        elif filename.endswith('.txt'): # inividual txt for each audio
            input_file = os.path.join(src_folder, filename)
            file_index = os.path.splitext(filename)[0].split('.')[0]
            with open(input_file, "r", encoding="utf-8") as file:
                line = file.readline()
            if cnt >= test_index:
                transcriptions.append((f"{id_0}_{id_1}_{file_index}", line, line, None, None, None, 20.0))
                # Clean and create a filename for the new text file
                filename = f"{dst_folder}/{id_0}_{id_1}_{file_index}.original.txt"
                with open(filename, "w", encoding="utf-8") as output_file:
                    output_file.write(line)
                filename = f"{dst_folder}/{id_0}_{id_1}_{file_index}.normalized.txt"
                with open(filename, "w", encoding='utf-8') as output_file:
                    output_file.write(line)
            else:
                test_transcriptions.append((f'{id_0}_{id_1}_{file_index}', line, line, None, None, None, 20.0))
                filename = f"{test_dst_folder}/{id_0}_{id_1}_{file_index}.original.txt"
                with open(filename, "w", encoding="utf-8") as output_file:
                    output_file.write(line)
                filename = f"{test_dst_folder}/{id_0}_{id_1}_{file_index}.normalized.txt"
                with open(filename, "w", encoding="utf-8") as output_file:
                    output_file.write(line)
    
    # tsv index file
    print(transcriptions)
    # Path to the TSV file
    tsv_file = f"{dst_folder}/{id_0}_{id_1}.trans.tsv"
    # Open the TSV file for writing
    with open(tsv_file, "w", newline="", encoding="utf-8") as file:
        for t in transcriptions:
            writer = csv.writer(file, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
            row = f"{t[0]}\t{t[1]}\t{t[2]}"
            writer.writerow(row.split("\t"))
    tsv_file = f"{dst_folder}/{id_0}_{id_1}.book.tsv"
    # Open the TSV file for writing
    with open(tsv_file, "w", newline="", encoding="utf-8") as file:
        for t in transcriptions:
            writer = csv.writer(file, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
            row = f"{t[0]}\t{t[1]}\t{t[2]}\t{t[3]}\t{t[4]}\t{t[5]}\t{t[6]}"
            writer.writerow(row.split("\t"))
    if test_transcriptions:
        tsv_file = f"{test_dst_folder}/{id_0}_{id_1}.trans.tsv"
        # Open the TSV file for writing
        with open(tsv_file, "w", newline="", encoding="utf-8") as file:
            for t in test_transcriptions:
                writer = csv.writer(file, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
                row = f"{t[0]}\t{t[1]}\t{t[2]}"
                writer.writerow(row.split("\t"))
        tsv_file = f"{test_dst_folder}/{id_0}_{id_1}.book.tsv"
        # Open the TSV file for writing
        with open(tsv_file, "w", newline="", encoding="utf-8") as file:
            for t in test_transcriptions:
                writer = csv.writer(file, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
                row = f"{t[0]}\t{t[1]}\t{t[2]}\t{t[3]}\t{t[4]}\t{t[5]}\t{t[6]}"
                writer.writerow(row.split("\t"))

if __name__ == '__main__':
    # m4a_to_wav()
    single_speaker_to_libriTTS_format()

            

