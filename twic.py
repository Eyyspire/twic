import os
import subprocess
import zipfile
import shutil

def create_directory(directory_path):
    """Creates a directory at the given path. Removes it if it already exists."""
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)
    os.makedirs(directory_path)

def download_with_curl(url, output_file):
    """Downloads a file using curl."""
    try:
        subprocess.run(['curl', '-L', '-o', output_file, url], check=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error downloading {url}: {e}")

def extract_and_cleanup(zip_file, extract_to):
    """Extracts the given ZIP file to a target folder and removes the ZIP afterward."""
    if os.path.exists(zip_file):
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        os.remove(zip_file)

def move_pgn_files(source_folder, destination_folder):
    """Moves .pgn files from source folder to destination folder."""
    pgn_files = [f for f in os.listdir(source_folder) if f.endswith('.pgn')]
    for pgn_file in pgn_files:
        shutil.move(os.path.join(source_folder, pgn_file), destination_folder)

def download_and_process_zip(number, destination_folder):
    """Downloads a ZIP file, extracts it, moves PGN files, and cleans up."""
    url = f"https://theweekinchess.com/zips/twic{number}g.zip"
    zip_file = f"twic{number}g.zip"
    extract_to = f"twic{number}g"

    download_with_curl(url, zip_file)
    extract_and_cleanup(zip_file, extract_to)
    move_pgn_files(extract_to, destination_folder)
    shutil.rmtree(extract_to)

def merge_pgn_files(destination_folder, merged_pgn_path):
    """Merges all PGN files in the destination folder into one."""
    with open(merged_pgn_path, 'w') as outfile:
        for pgn_file in os.listdir(destination_folder):
            if pgn_file.endswith('.pgn'):
                with open(os.path.join(destination_folder, pgn_file), 'r') as infile:
                    outfile.write(infile.read())

def clean_up_individual_pgns(destination_folder, merged_pgn_path):
    """Deletes all individual .pgn files except the merged one."""
    pgn_files = [f for f in os.listdir(destination_folder) if f.endswith('.pgn') and f != os.path.basename(merged_pgn_path)]
    for pgn_file in pgn_files:
        os.remove(os.path.join(destination_folder, pgn_file))

def main(start_number, end_number):
    """Main function to download, process, and merge PGN files for a given range."""
    downloaded_games_folder = os.path.join(os.getcwd(), "downloaded_games")
    create_directory(downloaded_games_folder)

    merged_pgn = os.path.join(downloaded_games_folder, f"all_games_{start_number}-{end_number}.pgn")
    if os.path.exists(merged_pgn):
        os.remove(merged_pgn)

    for number in range(start_number, end_number + 1):
        download_and_process_zip(number, downloaded_games_folder)

    merge_pgn_files(downloaded_games_folder, merged_pgn)
    
    clean_up_individual_pgns(downloaded_games_folder, merged_pgn)

    print(f"All files downloaded, unzipped, merged into {merged_pgn}, and individual files cleaned up successfully.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python script.py start_number [end_number]")
        sys.exit(1)

    start_number = int(sys.argv[1])
    end_number = int(sys.argv[2]) if len(sys.argv) > 2 else start_number

    main(start_number, end_number)
