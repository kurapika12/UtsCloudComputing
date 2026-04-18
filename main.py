import cli_github

def main():
    """
    File ini bertindak sebagai entry point utama aplikasi.
    Memanggil fungsi dari file cli_github.py.
    """
    try:
        cli_github.jalankan_cli()
    except KeyboardInterrupt:
        # Menangani jika user menekan Ctrl+C
        print("\n\n[Info] Program dihentikan oleh pengguna.")

if __name__ == "__main__":
    main()