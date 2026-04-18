import os
import requests
from dotenv import load_dotenv

def jalankan_cli():
    # 1. Load environment variables dari file .env
    load_dotenv()
    
    print("="*60)
    print("=== GitHub Repository Explorer ===")
    print("="*60)
    
    # Meminta input username dari user melalui terminal
    username = input("Masukkan username GitHub: ").strip()

    if not username:
        print("[Error] Username tidak boleh kosong!")
        return

    # 2. Mengambil API key dari .env
    api_key = os.getenv("GITHUB_API_KEY")

    # 3. Setup headers
    # Menggunakan standar API GitHub v3
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }

    # 4. Logika Authenticated vs Public Fallback
    if api_key:
        print("[Info] Menggunakan Authenticated Request (API Key ditemukan).")
        headers["Authorization"] = f"Bearer {api_key}"
    else:
        print("[Info] Menggunakan Public API (Tidak ada API Key).")

    # Endpoint untuk mengambil daftar repository dari sebuah user
    url = f"https://api.github.com/users/{username}/repos"

    try:
        print("Mengambil data dari GitHub...\n")
        response = requests.get(url, headers=headers)

        # 5. Penanganan Error Sederhana
        if response.status_code == 200:
            repos = response.json()

            if not repos:
                print(f"User '{username}' tidak memiliki public repository.")
                return

            # 6. Format Output sebagai Tabel Rapi
            # Menggunakan string formatting Python: :<35 berarti rata kiri dengan lebar 35 karakter
            print(f"{'Nama Repository':<35} | {'Visibility':<10} | {'Bintang':<7}")
            print("-" * 60)

            # Looping data repositori
            for repo in repos:
                name = repo.get("name", "")
                # Potong nama repo jika terlalu panjang agar tabel tidak rusak
                if len(name) > 34:
                    name = name[:31] + "..."

                visibility = repo.get("visibility", "public")
                stars = repo.get("stargazers_count", 0)

                print(f"{name:<35} | {visibility:<10} | {stars:<7}")
                
            print("-" * 60)
            print(f"Total Repositori: {len(repos)}")

        elif response.status_code == 404:
            print(f"[Error] User '{username}' tidak ditemukan di GitHub.")
        elif response.status_code == 401:
            print("[Error] API Key tidak valid (Unauthorized). Silakan periksa GITHUB_API_KEY di .env Anda.")
        elif response.status_code == 403:
            print("[Error] Terkena limit API GitHub (Rate Limit Exceeded). Gunakan API Key untuk limit lebih besar.")
        else:
            print(f"[Error] Gagal mengambil data. HTTP Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"[Error] Terjadi kesalahan koneksi jaringan: {e}")

if __name__ == "__main__":
    jalankan_cli()