import os
import subprocess
import socket
import time
import psutil  # pip install psutil

# ==== 1️⃣ Path backend store untuk MLflow ====
STORE = r"file:C:\Users\student\Documents\Scheduling_Puma_Optimizer\notebooks\mlruns"

# ==== 2️⃣ Port yang akan digunakan ====
PORT = 5000


# ==== 3️⃣ Fungsi untuk menutup proses lama di port tertentu ====
def kill_process_on_port(port):
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            connections = proc.connections(kind='inet')
            for conn in connections:
                if conn.laddr.port == port:
                    print(f"🔴 Menutup proses lama di port {port} (PID {proc.pid}) ...")
                    proc.kill()
                    break
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue


kill_process_on_port(PORT)


# ==== 4️⃣ Jalankan MLflow UI ====
cmd = [
    "python", "-m", "mlflow", "ui",
    "--host", "127.0.0.1",
    "--port", str(PORT),
    "--backend-store-uri", STORE,
]

print("🚀 Menjalankan MLflow UI...")
process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

# ==== 5️⃣ Tunggu sampai port aktif ====
for _ in range(60):
    sock = socket.socket()
    result = sock.connect_ex(("127.0.0.1", PORT))
    sock.close()
    if result == 0:
        break
    time.sleep(0.5)

print(f"✅ MLflow UI aktif di: http://127.0.0.1:{PORT}")
print("Tekan Ctrl+C di terminal VS Code untuk menghentikan server.\n")

# ==== 6️⃣ Tampilkan log MLflow di terminal ====
try:
    for line in process.stdout:
        print(line, end="")
except KeyboardInterrupt:
    print("\n🛑 Dihentikan oleh pengguna. Menutup MLflow...")
    process.terminate()