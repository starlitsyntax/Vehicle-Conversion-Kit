import tkinter as tk
from tkinter import ttk, messagebox
import serial
import serial.tools.list_ports


class SwitchGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Toggle Switch Control")
        self.root.resizable(False, False)
        self.serial = None

        self._build_ui()

    def _build_ui(self):
        root = self.root
        root.configure(bg="#f0f0f0")

        pad = {"padx": 16, "pady": 10}

        # ── Port selector ──────────────────────────────────────────
        port_frame = tk.Frame(root, bg="#f0f0f0")
        port_frame.pack(**pad)

        tk.Label(port_frame, text="Port:", bg="#f0f0f0", font=("Helvetica", 11)).pack(side="left")

        self.port_var = tk.StringVar()
        self.port_combo = ttk.Combobox(port_frame, textvariable=self.port_var, width=18,
                                       font=("Helvetica", 11), state="readonly")
        self.port_combo.pack(side="left", padx=(6, 0))

        tk.Button(port_frame, text="⟳", font=("Helvetica", 11), relief="flat",
                  bg="#f0f0f0", cursor="hand2",
                  command=self._refresh_ports).pack(side="left", padx=(4, 0))

        # ── Connect button ─────────────────────────────────────────
        self.connect_btn = tk.Button(root, text="Connect", font=("Helvetica", 11, "bold"),
                                     width=14, relief="flat", bg="#4a90d9", fg="white",
                                     activebackground="#357abd", activeforeground="white",
                                     cursor="hand2", command=self._toggle_connection)
        self.connect_btn.pack(pady=(0, 4))

        # ── Divider ────────────────────────────────────────────────
        ttk.Separator(root, orient="horizontal").pack(fill="x", padx=16, pady=8)

        # ── ON / OFF buttons ───────────────────────────────────────
        btn_frame = tk.Frame(root, bg="#f0f0f0")
        btn_frame.pack(padx=20, pady=10)

        btn_cfg = dict(font=("Helvetica", 18, "bold"), width=7, height=2,
                       relief="flat", cursor="hand2", state="disabled")

        self.on_btn = tk.Button(btn_frame, text="ON",
                                bg="#2ecc71", fg="white",
                                activebackground="#27ae60", activeforeground="white",
                                command=self._send_on, **btn_cfg)
        self.on_btn.pack(side="left", padx=10)

        self.off_btn = tk.Button(btn_frame, text="OFF",
                                 bg="#e74c3c", fg="white",
                                 activebackground="#c0392b", activeforeground="white",
                                 command=self._send_off, **btn_cfg)
        self.off_btn.pack(side="left", padx=10)

        # ── Status bar ─────────────────────────────────────────────
        ttk.Separator(root, orient="horizontal").pack(fill="x", padx=16, pady=(10, 0))

        self.status_var = tk.StringVar(value="Not connected")
        tk.Label(root, textvariable=self.status_var, bg="#f0f0f0",
                 font=("Helvetica", 10), fg="#666666").pack(pady=(4, 10))

        self._refresh_ports()

    # ── Port helpers ───────────────────────────────────────────────

    def _refresh_ports(self):
        ports = [p.device for p in serial.tools.list_ports.comports()]
        self.port_combo["values"] = ports
        if ports:
            self.port_var.set(ports[0])
        else:
            self.port_var.set("")

    # ── Connection ─────────────────────────────────────────────────

    def _toggle_connection(self):
        if self.serial and self.serial.is_open:
            self._disconnect()
        else:
            self._connect()

    def _connect(self):
        port = self.port_var.get()
        if not port:
            messagebox.showerror("No port", "Select a COM port first.")
            return
        try:
            self.serial = serial.Serial(port, 9600, timeout=1)
            self.connect_btn.config(text="Disconnect", bg="#e67e22", activebackground="#ca6f1e")
            self.on_btn.config(state="normal")
            self.off_btn.config(state="normal")
            self.status_var.set(f"Connected — {port}")
        except serial.SerialException as e:
            messagebox.showerror("Connection error", str(e))

    def _disconnect(self):
        if self.serial:
            self.serial.close()
        self.connect_btn.config(text="Connect", bg="#4a90d9", activebackground="#357abd")
        self.on_btn.config(state="disabled")
        self.off_btn.config(state="disabled")
        self.status_var.set("Not connected")

    # ── Send commands ──────────────────────────────────────────────

    def _send(self, command):
        if self.serial and self.serial.is_open:
            self.serial.write((command + "\n").encode("utf-8"))
            self.serial.flush()
            self.status_var.set(f"Sent: '{command}'")
        else:
            messagebox.showwarning("Not connected", "Connect to a port first.")

    def _send_on(self):
        self._send("on")

    def _send_off(self):
        self._send("off")


if __name__ == "__main__":
    root = tk.Tk()
    app = SwitchGUI(root)
    root.mainloop()
