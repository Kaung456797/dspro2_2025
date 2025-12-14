import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from cryptography.fernet import Fernet

def generate_key(password):
    # パスワードから鍵を作成（簡易版）
    return Fernet(base64.urlsafe_b64encode(password.ljust(32)[:32].encode()))

def encrypt(text, password):
    f = generate_key(password)
    return f.encrypt(text.encode())

def decrypt(token, password):
    f = generate_key(password)
    return f.decrypt(token).decode()

def save_encrypted():
    password = simpledialog.askstring("パスワード", "パスワードを入力（保存時も必要）:", show="*")
    if not password:
        return
    data = text_area.get("1.0", tk.END)

    encrypted = encrypt(data, password)

    filepath = filedialog.asksaveasfilename(defaultextension="enc",
                        filetypes=[("Encrypted Files", "*.enc")])
    if filepath:
        with open(filepath, "wb") as f:
            f.write(encrypted)
        messagebox.showinfo("保存", "暗号化して保存しました！")

def open_encrypted():
    filepath = filedialog.askopenfilename(filetypes=[("Encrypted Files", "*.enc")])
    if not filepath:
        return

    password = simpledialog.askstring("パスワード", "パスワードを入力してください:", show="*")
    if not password:
        return

    try:
        with open(filepath, "rb") as f:
            encrypted = f.read()
        decrypted = decrypt(encrypted, password)

        text_area.delete("1.0", tk.END)
        text_area.insert(tk.END, decrypted)
    except:
        messagebox.showerror("エラー", "パスワードが違います。")

root = tk.Tk()
root.title("暗号化メモ帳")
root.geometry("700x500")

text_area = tk.Text(root, wrap="word")
text_area.pack(expand=True, fill="both")

menu_bar = tk.Menu(root)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="暗号化ファイルを開く", command=open_encrypted)
file_menu.add_command(label="暗号化して保存", command=save_encrypted)
menu_bar.add_cascade(label="ファイル", menu=file_menu)

root.config(menu=menu_bar)

root.mainloop()