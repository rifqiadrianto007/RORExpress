import psycopg2
import pandas as pd
import os
import random
from stdiomask import getpass
from colorama import init, Fore, Style
from tabulate import tabulate

# Inisialisasi Colorama untuk dukungan warna pada terminal
init(autoreset=True)

# Fungsi untuk membersihkan layar terminal
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Fungsi untuk menghubungkan ke database
def connect():
    return psycopg2.connect(
        database="DB_ALGO", 
        user="postgres",  
        password="010603", 
        host="localhost",
        port="5432"
    )

# Fungsi untuk registrasi pengguna baru
def register():
    clear_screen()
    print(Fore.CYAN + "=== Registrasi Pengguna Baru ===")
    conn = connect()
    cur = conn.cursor()
    username = input("Masukkan username: ")
    password = getpass("Masukkan password: ")
    role = "user"  # Secara otomatis mengatur role sebagai 'user'

    try:
        cur.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, password, role))
        conn.commit()
        print(Fore.GREEN + "Registrasi berhasil!")
    except psycopg2.Error as e:
        print(Fore.RED + f"Error: {e}")
    finally:
        cur.close()
        conn.close()
# Fungsi untuk login
def login():
    clear_screen()
    print(Fore.CYAN + "\n=== Login ===")
    conn = connect()
    cur = conn.cursor()
    username = input("Masukkan username: ")
    password = getpass("Masukkan password: ")

    cur.execute("SELECT id, role FROM users WHERE username = %s AND password = %s", (username, password))
    user = cur.fetchone()

    if user:
        print(Fore.GREEN + "Login berhasil!")
        return user
    else:
        print(Fore.RED + "Username atau password salah.")
        return None

# Fungsi untuk memasukkan data barang (hanya untuk user)
def input_data(user_id):
    clear_screen()
    print(Fore.CYAN + "\n=== Masukkan Data Barang ===")
    conn = connect()
    cur = conn.cursor()
    
    try:
        berat = float(input("Masukkan berat barang (kg): "))
        barang = input("Masukkan nama barang: ")
        harga = int(input("Masukkan harga barang (total dalam Rupiah): "))

        cur.execute("INSERT INTO data_barang (user_id, berat, barang, harga) VALUES (%s, %s, %s, %s)", (user_id, berat, barang, harga))
        conn.commit()
        print(Fore.GREEN + "Data barang berhasil dimasukkan!")
    except ValueError:
        print(Fore.RED + "Input tidak valid, pastikan berat dan harga diisi dengan angka yang benar.")
    except psycopg2.Error as e:
        print(Fore.RED + f"Error: {e}")
    finally:
        cur.close()
        conn.close()
        

def delete_dataBarang():
    clear_screen()
    print(Fore.CYAN + "\n=== Hapus Data Barang ===")
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM data_barang")
        rows = cur.fetchall()
        headers = [desc[0] for desc in cur.description]
        print(tabulate(rows, headers=headers, tablefmt="fancy_grid"))
        
        barang_id = input("Masukkan ID barang yang ingin dihapus: ")
        
        cur.execute("SELECT 1 FROM data_barang WHERE id = %s", (barang_id,))
        if cur.fetchone() is None:
            print(Fore.RED + "Error: ID barang tidak ditemukan.")
            return

        confirm = input(Fore.RED + "Apakah Anda yakin ingin menghapus data ini? (y/n): ")
        if confirm.lower() == 'y':
            cur.execute("DELETE FROM data_barang WHERE id = %s", (barang_id,))
            conn.commit()
            print(Fore.GREEN + "Data barang berhasil dihapus!")
        else:
            print(Fore.YELLOW + "Penghapusan data dibatalkan.")
    except psycopg2.Error as e:
        print(Fore.RED + f"Error: {e}")
    finally:
        cur.close()
        conn.close()

def update_dataBarang():
    clear_screen()
    print(Fore.CYAN + "\n=== Update Data Barang ===")
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM data_barang")
        rows = cur.fetchall()
        headers = [desc[0] for desc in cur.description]
        print(tabulate(rows, headers=headers, tablefmt="fancy_grid"))
        
        barang_id = input("Masukkan ID barang yang ingin diupdate: ")
        
        cur.execute("SELECT 1 FROM data_barang WHERE id = %s", (barang_id,))
        if cur.fetchone() is None:
            print(Fore.RED + "Error: ID barang tidak ditemukan.")
            return

        berat = input("Masukkan berat barang baru: ")
        barang = input("Masukkan nama barang baru: ")
        harga = input("Masukkan harga barang baru: ")
        
        cur.execute("UPDATE data_barang SET berat = %s, barang = %s, harga = %s WHERE id = %s", (berat, barang, harga, barang_id))
        conn.commit()
        print(Fore.GREEN + "Data barang berhasil diupdate!")
    except psycopg2.Error as e:
        print(Fore.RED + f"Error: {e}")
    finally:
        cur.close()
        conn.close()
        
def linear_search(df, search_term):
    search_term_lower = search_term.lower()
    matching_rows = []

    for index, row in df.iterrows():
        barang_value = str(row['barang']).lower()
        if search_term_lower in barang_value:
            matching_rows.append(row.values.tolist())

    if matching_rows:
        print(tabulate(matching_rows, headers=df.columns, tablefmt='fancy_grid'))
        input(Fore.GREEN + "Tekan Enter untuk melanjutkan...")
    else:
        print(Fore.YELLOW + "Data barang tidak ditemukan.")
        input(Fore.GREEN + "Tekan Enter untuk melanjutkan...")
        
def bubble_sort(df, column):
    n = len(df)
    for i in range(n):
        for j in range(0, n-i-1):
            if df.iloc[j][column] > df.iloc[j+1][column]:
                # Swap rows
                temp = df.iloc[j].copy()
                df.iloc[j] = df.iloc[j+1]
                df.iloc[j+1] = temp
    return df.values.tolist() 

def view_data():
    while True:
        clear_screen()
        print(Fore.CYAN + "\n=== Lihat Semua Data Barang ===")
        conn = connect()
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM data_barang")
            rows = cur.fetchall()
            headers = [desc[0] for desc in cur.description]
            df = pd.DataFrame(rows, columns=headers)

            print(tabulate(df, headers='keys', tablefmt='fancy_grid'))

            print("1. Update Data Barang")
            print("2. Hapus Data Barang")
            print("3. Cari Data Barang")
            print("4. Urutkan Data Barang")
            print("5. Kembali")
            choice = input(Fore.YELLOW + "Pilih opsi: ")

            if choice == "1":
                update_dataBarang()
            elif choice == "2":
                delete_dataBarang()
            elif choice == "3":
                search_term = input("Masukkan nama search_term yang dicari: ")
                linear_search(df, search_term)
            elif choice == "4":
                column = input("Pilih kolom untuk pengurutan (berat/harga): ")
                if column in ['berat', 'harga']:
                    sorted_data = bubble_sort(df, column)
                    print(tabulate(sorted_data, headers=df.columns, tablefmt='fancy_grid'))
                    input(Fore.GREEN + "Tekan Enter untuk melanjutkan...") 
                else:
                    print(Fore.RED + "Kolom tidak valid.")
                    input(Fore.GREEN + "Tekan Enter untuk melanjutkan...") 
            elif choice == "5":
                admin_menu()
            else:
                print(Fore.RED + "Opsi tidak valid.")
                input(Fore.GREEN + "Tekan Enter untuk melanjutkan...") 
        except psycopg2.Error as e:
            print(Fore.RED + f"Error: {e}")
            input(Fore.GREEN + "Tekan Enter untuk melanjutkan...")  
        finally:
            cur.close()
            conn.close()
           
def baca_database():
    conn = connect()
    query = "SELECT * FROM data_barang WHERE keterangan = 'BELUM DIKIRIM'"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Fungsi knapsack 0/1
def knapsack_01(items, max_weight):
    n = len(items)
    K = [[0 for x in range(max_weight + 1)] for x in range(n + 1)]

    for i in range(n + 1):
        for w in range(max_weight + 1):
            if i == 0 or w == 0:
                K[i][w] = 0
            elif items[i-1]['weight'] <= w:
                K[i][w] = max(items[i-1]['weight'] + K[i-1][int(w-items[i-1]['weight'])], K[i-1][w])
            else:
                K[i][w] = K[i-1][w]

    res = K[n][max_weight]
    w = max_weight
    selected_items = []

    for i in range(n, 0, -1):
        if res <= 0:
            break
        if res == K[i-1][w]:
            continue
        else:
            selected_items.append(items[i-1])
            res = res - items[i-1]['weight']
            w = w - int(items[i-1]['weight'])

    return K[n][max_weight], selected_items

def rekomendasi_barang():
    clear_screen()
    df = baca_database()

    if df.empty:
        input("Tidak ada data yang dapat diproses. Tekan Enter untuk kembali.")
        return

    try:
        print("==========PILIH JENIS TRANSPORTASI==========\n")
        print("1. Motor (0.1 - 2.0 kg, Max 10 kg)")
        print("2. Cargo (2.1 - 5.0 kg, Max 100 kg)")
        print("3. Truck (Di atas 5.0 kg, Max 300 kg)")
        pilih = input("\nMasukkan transportasi yang akan digunakan : ")

        if pilih == "1":
            min_berat = 0.1
            max_berat = 2.0
            berat_total = 10
        elif pilih == "2":
            min_berat = 2.1
            max_berat = 10.0
            berat_total = 100
        elif pilih == "3":
            min_berat = 5.1
            max_berat = 10.0
            berat_total = 500
        else:
            input("Pilihan tidak valid. Tekan Enter untuk kembali.")
            return
    except ValueError:
        input("Input tidak valid. Tekan Enter untuk kembali.")
        return

    print(f"Min berat: {min_berat}, Max berat: {max_berat}, Berat total: {berat_total}")
    items = [{"name": row['barang'], "price": row['harga'], "weight": float(row['berat'])} for index, row in df.iterrows()]
    items = [item for item in items if min_berat <= item["weight"] <= max_berat and not pd.isnull(item["price"])]
    
    if not items:
        print("Tidak ada barang yang dapat dibeli dengan berat tersebut.")
        input("Tekan Enter untuk kembali.")
    else:
        max_price, selected_items = knapsack_01(items, berat_total)

        unit = 'kg'
        print("Barang yang dipilih:")

        total_price = sum(item["price"] for item in selected_items)
        total_weight = sum(item["weight"] for item in selected_items)

        if total_weight > berat_total:
            print("Tidak ada kombinasi barang yang memenuhi kapasitas maksimum transportasi.")
        else:
            table = []

            for item in selected_items:
                table.append([item["name"], item["price"], item["weight"]])
                updatestatus(item["name"])

            print(tabulate(table, headers=["Barang", "Harga (Rp)", f"Berat ({unit})"], tablefmt="fancy_grid"))
            print(f"Total harga: {total_price} Rupiah")
            print(f"Total berat: {total_weight} {unit}")

            input(f"Barang di atas merupakan barang yang Anda dapatkan dengan berat total maksimal {berat_total} kg. Tekan Enter untuk melanjutkan")
            admin_menu()

def updatestatus(namabarang):
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE data_barang SET keterangan = 'Sudah Dikirim' WHERE barang ilike %s and keterangan = 'BELUM DIKIRIM'", (namabarang,))
        conn.commit()
    except psycopg2.Error as e:
        print(Fore.RED + f"Error: {e}")
    finally:
        cur.close()
        conn.close()

def admin_menu():
    clear_screen()
    print(Fore.CYAN + "\n=== Menu Admin ===")
    print("1. Lihat Semua Data Barang")
    print("2. Rekomendasi Barang (Knapsack)")
    choice = input(Fore.YELLOW + "Pilih opsi: ")

    if choice == "1":
        view_data()
    elif choice == "2":
        rekomendasi_barang()
    else:
        print(Fore.RED + "Opsi tidak valid. Kembali ke menu utama.")

clear_screen()
print(Fore.YELLOW + "=== Selamat Datang di RAWR EXPRESS ===")

login_success = False
while not login_success:
    print("Menu Utama:")
    print("1. " + Fore.GREEN + "Register")
    print("2. " + Fore.GREEN + "Login")
    choice = input(Fore.YELLOW + "Pilih opsi: ")

    if choice == "1":
        register()
    elif choice == "2":
        user = login()
        if user:
            user_id, role = user
            login_success = True
            if role == "admin":
                print(Fore.YELLOW + "Anda telah login sebagai admin.")
                admin_menu()
            elif role == "user":
                print(Fore.YELLOW + "Anda telah login sebagai user.")
                input_data(user_id)
                rekomendasi_barang()
    else:
        print(Fore.RED + "Opsi tidak valid.")
