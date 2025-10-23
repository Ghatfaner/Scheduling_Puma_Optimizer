import subprocess
import os
import sys

# --- KONFIGURASI ---
NOTEBOOK_FILE = "pso_aco_abc_puma_mlflow_ti.ipynb"
NUM_RUNS = 20
# -----------------

def run_notebook(notebook_path, output_path, iteration):
    """Menjalankan satu file notebook menggunakan nbconvert."""
    
    # Perintah ini akan menjalankan notebook dan menyimpan outputnya
    # --ExecutePreprocessor.timeout=-1 berarti tidak ada batasan waktu
    command = [
        sys.executable, "-m", "jupyter", "nbconvert",
        "--to", "notebook",
        "--execute",
        "--output", output_path,
        "--ExecutePreprocessor.timeout=-1",
        notebook_path
    ]
    
    print(f"[INFO] Memulai Eksekusi ke-{iteration}...")
    print(f"[CMD] {' '.join(command)}")
    
    try:
        # Menjalankan perintah
        subprocess.run(command, check=True)
        print(f"[SUCCESS] Eksekusi ke-{iteration} SELESAI. Output disimpan di {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"!!! [ERROR] GAGAL PADA EKSEKUSI KE-{iteration}: {e} !!!")
        print("Menghentikan skrip. Periksa error di atas atau di file notebook output.")
        return False
    except FileNotFoundError:
        print("!!! [ERROR] Perintah 'jupyter' tidak ditemukan.")
        print("Pastikan 'jupyter' dan 'nbconvert' terinstal di lingkungan Python Anda.")
        print("Coba jalankan: pip install jupyter nbconvert")
        return False

def main():
    # Pastikan file notebook ada
    if not os.path.exists(NOTEBOOK_FILE):
        print(f"!!! [ERROR] File notebook tidak ditemukan: {NOTEBOOK_FILE}")
        print("Pastikan skrip ini ada di direktori yang sama dengan file .ipynb Anda.")
        return

    print(f"--- Skrip Otomatisasi Dimulai ---")
    print(f"Target Notebook: {NOTEBOOK_FILE}")
    print(f"Total Eksekusi: {NUM_RUNS}")
    print("--------------------------------------")

    for i in range(NUM_RUNS):
        iteration_num = i + 1
        
        # Buat nama file output yang unik untuk setiap eksekusi
        # Ini penting agar Anda bisa memeriksa output jika terjadi error
        output_filename = f"executed_output_{iteration_num}.ipynb"
        
        success = run_notebook(NOTEBOOK_FILE, output_filename, iteration_num)
        
        if not success:
            # Jika satu eksekusi gagal, hentikan seluruh proses
            break
            
    print("--------------------------------------")
    print("--- Skrip Otomatisasi Selesai. ---")

if __name__ == "__main__":
    # Peringatan penting tentang direktori
    if "mlruns" in os.getcwd():
        print("!!! [PERINGATAN KERAS] !!!")
        print("Anda menjalankan skrip ini dari dalam direktori 'mlruns'.")
        print("Ini akan menyebabkan error. Harap pindah ke direktori 'notebooks' (satu level di atas)")
        print("dan jalankan skrip ini dari sana.")
    else:
        main()