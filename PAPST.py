#Particle Analysis Physics Simulation Tool
import tkinter as tk
from tkinter import messagebox, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
class PAPSTApp:
    def _init_(self, root):
        self.root = root
        self.root.title("PAPST")
        self.container = ttk.Frame(self.root)
        self.container.pack(fill="both", expand=True)
        self.show_main_menu()
    def clear_container(self):
        for widget in self.container.winfo_children(): widget.destroy()
    def show_main_menu(self):
        self.clear_container()
        frame = ttk.Frame(self.container)
        frame.pack(expand=True)
        ttk.Label(frame, text="PAPST").pack()
        ttk.Label(frame, text="Particle Analysis Physics Simulation Tool").pack()
        ttk.Button(frame, text="Macroscopic Particle", command=self.show_macro_submenu).pack()
        ttk.Button(frame, text="Microscopic Particle", command=self.show_micro_stub).pack()
        ttk.Button(frame, text="Exit", command=self.root.quit).pack()
    def show_macro_submenu(self):
        self.clear_container()
        frame = ttk.Frame(self.container)
        frame.pack(expand=True)
        ttk.Label(frame, text="Macroscopic Particle").pack()
        ttk.Button(frame, text="Point sized Particle in 1 dimesion", command=lambda: self.show_kinematics_screen(1)).pack()
        ttk.Button(frame, text="Point sized Particle in 2 dimesions", command=lambda: self.show_kinematics_screen(2)).pack()
        ttk.Button(frame, text="Point sized Particle in 3 dimesions", command=lambda: self.show_kinematics_screen(3)).pack()
        ttk.Button(frame, text="Collision in 1 dimesion", command=self.show_collision_screen).pack()
        ttk.Button(frame, text="Back", command=self.show_main_menu).pack()
    def show_micro_stub(self):
        messagebox.showinfo("Microscopic Particle")
    def show_kinematics_screen(self, dim):
        self.clear_container()
        self.current_dim = dim
        hdr_frame = ttk.Frame(self.container)
        hdr_frame.pack(fill="x")
        ttk.Label(hdr_frame, text=f"Macroscopic Particle: {dim}D Motion Analysis").pack(side="left")
        ttk.Button(hdr_frame, text="Back", command=self.show_macro_submenu).pack(side="right")
        main_body = ttk.Frame(self.container)
        main_body.pack(fill="both", expand=True)
        input_panel = ttk.LabelFrame(main_body, text="Input Parameters")
        input_panel.pack(side="left", fill="both")
        self.entries = {}
        axes = ["X", "Y", "Z"][:dim]
        def add_vec_input(parent, label_text, default_vals):
            frame = ttk.Frame(parent)
            frame.pack(fill="x")
            ttk.Label(frame, text=label_text).pack(side="left")
            entries = []
            for i, axis in enumerate(axes):
                ttk.Label(frame, text=f"{axis}:").pack(side="left")
                e = ttk.Entry(frame, width=6)
                e.insert(0, str(default_vals[i]))
                e.pack(side="left")
                entries.append(e)
            return entries
        def add_scalar_input(parent, label_text, default_val=""):
            frame = ttk.Frame(parent)
            frame.pack(fill="x")
            ttk.Label(frame, text=label_text).pack(side="left")
            e = ttk.Entry(frame, width=12)
            if default_val != "": e.insert(0, str(default_val))
            e.pack(side="left")
            return e
        self.entries["r0"] = add_vec_input(input_panel, "Initial Position r₀ (m):", [0.0] * dim)
        self.entries["v0"] = add_vec_input(input_panel, "Initial Velocity v₀ (m/s):", [0.0] * dim)
        self.entries["a0"] = add_vec_input(input_panel, "Initial Acceleration a₀ (m/s²):", [0.0] * dim)
        ttk.Separator(input_panel, orient="horizontal").pack(fill="x")
        self.entries["t0"] = add_scalar_input(input_panel, "Initial Time t₀ (s):", "0.0")
        self.entries["tf"] = add_scalar_input(input_panel, "Final Time t_f (s):", "10.0")
        self.entries["m"] = add_scalar_input(input_panel, "Mass m (kg):", "")
        ttk.Button(input_panel, text="Calculate/Simulate", command=self.calculate_kinematics).pack(fill="x")
        output_panel = ttk.LabelFrame(main_body, text="Calculated Parameters")
        output_panel.pack(side="right", fill="both", expand=True)
        canvas = tk.Canvas(output_panel)
        scrollbar = ttk.Scrollbar(output_panel, orient="vertical", command=canvas.yview)
        self.out_frame = ttk.Frame(canvas)
        self.out_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.out_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.out_labels = {}
        out_specs = [
            ("pos", "Final Position (r_f):", "Displacement (Δr):"),
            ("vel", "Final Velocity (v_f):", "Average Velocity (v_avg):"),
            ("acc", "Final Acceleration (a_f):", None),
            ("force", "Net Force (F_net):", None),
            ("impulse", "Impulse (J):", None),
            ("momentum", "Net Linear Momentum (p):", None),
            ("ke", "Initial Kinetic Energy (KE_i):", "Final KE (KE_f):"),
            ("work", "Work Done / ΔKE (W):", None),
            ("power", "Final Power (P_f):", "Average Power (P_avg):")
        ]
        for key, lbl1_text, lbl2_text in out_specs:
            row = ttk.Frame(self.out_frame)
            row.pack(fill="x")
            ttk.Button(row, text="(i)", width=3, command=lambda k=key: show_info(k)).pack(side="left")
            f_labels = ttk.Frame(row)
            f_labels.pack(side="left", fill="x", expand=True)
            l1 = ttk.Label(f_labels, text=f"{lbl1_text} ")
            l1.pack(anchor="w")
            self.out_labels[f"{key}_1"] = l1
            if lbl2_text:
                l2 = ttk.Label(f_labels, text=f"{lbl2_text} ")
                l2.pack(anchor="w")
                self.out_labels[f"{key}_2"] = l2
        sim_trigger_frame = ttk.Frame(self.container)
        sim_trigger_frame.pack(fill="x")
        self.btn_sim = ttk.Button(sim_trigger_frame, text="Simulation", state="disabled", command=self.open_simulation_window)
        self.btn_sim.pack(side="right")
    def show_collision_screen(self):
        self.clear_container()
        hdr_frame = ttk.Frame(self.container)
        hdr_frame.pack(fill="x")
        ttk.Label(hdr_frame, text="Macroscopic Particle: Collision in 1D").pack(side="left")
        ttk.Button(hdr_frame, text="Back", command=self.show_macro_submenu).pack(side="right")
        main_body = ttk.Frame(self.container)
        main_body.pack(fill="both", expand=True)
        input_panel = ttk.LabelFrame(main_body, text=" Input Parameters ")
        input_panel.pack(side="left", fill="both")
        self.col_entries = {}
        def add_col_field(parent, label_text, default_val=""):
            frame = ttk.Frame(parent)
            frame.pack(fill="x")
            ttk.Label(frame, text=label_text).pack(side="left")
            e = ttk.Entry(frame, width=12)
            if default_val != "": e.insert(0, str(default_val))
            e.pack(side="left")
            return e
        ttk.Label(input_panel, text="Particle 1").pack(anchor="w")
        self.col_entries["m1"] = add_col_field(input_panel, "Mass m₁ (kg):", "")
        self.col_entries["x1"] = add_col_field(input_panel, "Initial Position x₁ (m):", "0.0")
        self.col_entries["v1"] = add_col_field(input_panel, "Initial Velocity v₁ (m/s):", "0.0")
        ttk.Separator(input_panel, orient="horizontal").pack(fill="x")
        ttk.Label(input_panel, text="Particle 2").pack(anchor="w")
        self.col_entries["m2"] = add_col_field(input_panel, "Mass m₂ (kg):", "")
        self.col_entries["x2"] = add_col_field(input_panel, "Initial Position x₂ (m):", "0.0")
        self.col_entries["v2"] = add_col_field(input_panel, "Initial Velocity v₂ (m/s):", "0.0")
        ttk.Separator(input_panel, orient="horizontal").pack(fill="x")
        ttk.Label(input_panel, text="System Dynamics").pack(anchor="w")
        self.col_entries["t0"] = add_col_field(input_panel, "Initial Time t₀ (s):", "0.0")
        self.col_entries["e"] = add_col_field(input_panel, "Restitution Coefficient (e):", "1.0")
        ttk.Button(input_panel, text="Calculate", command=self.calculate_collision).pack(fill="x")
        output_panel = ttk.LabelFrame(main_body, text="Calculated/simulate")
        output_panel.pack(side="right", fill="both", expand=True)
        self.col_out_labels = {}
        out_rows = [
            ("t_dt", "Time for Collision (Δt_coll):", "Time of Collision (t_coll):"),
            ("pos", "Position at Collision (x_coll):", None),
            ("v1f", "Particle 1 Final Vel (v1f):", None),
            ("v2f", "Particle 2 Final Vel (v2f):", None),
            ("ke", "Initial System KE (KE_i):", "Final System KE (KE_f):"),
            ("loss", "Kinetic Energy Lost (ΔKE):", None)
        ]
        for key, lbl1, lbl2 in out_rows:
            row = ttk.Frame(output_panel)
            row.pack(fill="x")
            ttk.Button(row, text="(i)", width=3, command=lambda: show_info("collision")).pack(side="left")
            f_lbls = ttk.Frame(row)
            f_lbls.pack(side="left", fill="x", expand=True)
            l1 = ttk.Label(f_lbls, text=f"{lbl1} --")
            l1.pack(anchor="w")
            self.col_out_labels[f"{key}_1"] = l1
            if lbl2:
                l2 = ttk.Label(f_lbls, text=f"{lbl2} --")
                l2.pack(anchor="w")
                self.col_out_labels[f"{key}_2"] = l2
        sim_trigger_frame = ttk.Frame(self.container)
        sim_trigger_frame.pack(fill="x")
        self.btn_col_sim = ttk.Button(sim_trigger_frame, text="Simulation", state="disabled", command=self.open_collision_simulation_window)
        self.btn_col_sim.pack(side="right")
    def open_simulation_window(self):
        r0, v0, a0, t0, tf = self.calc_data
        sim_win = tk.Toplevel(self.root)
        sim_win.title(f"Simulation of the collision")
        ctrl_frame = ttk.LabelFrame(sim_win, text=" Simulation Window Control ")
        ctrl_frame.pack(fill="x")
        ttk.Label(ctrl_frame, text=f"Calculated Interval: [{t0:.1f}s, {tf:.1f}s]").pack(side="left")
        f_inputs = ttk.Frame(ctrl_frame)
        f_inputs.pack(side="right")
        ttk.Label(f_inputs, text="Sim Start:").pack(side="left")
        e_sim_start = ttk.Entry(f_inputs, width=6)
        e_sim_start.insert(0, str(t0))
        e_sim_start.pack(side="left")
        ttk.Label(f_inputs, text="Sim End:").pack(side="left")
        e_sim_end = ttk.Entry(f_inputs, width=6)
        e_sim_end.insert(0, str(min(tf, t0 + 10.0)))
        e_sim_end.pack(side="left")
        plot_frame = ttk.Frame(sim_win)
        plot_frame.pack(fill="both", expand=True)
        fig = plt.figure()
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        slider_frame = ttk.Frame(sim_win)
        slider_frame.pack(fill="x")
        lbl_time = ttk.Label(slider_frame, text="Time t = 0.0s")
        lbl_time.pack()
        slider = ttk.Scale(slider_frame, from_=t0, to=tf, orient="horizontal")
        slider.pack(fill="x")
        f_inputs.children["!button"] = ttk.Button(f_inputs, text="Apply", command=apply_sim_window)
        f_inputs.children["!button"].pack(side="left")
        slider.config(command=update_plot)
        apply_sim_window()
    def open_collision_simulation_window(self):
        m1, m2, x1, x2, v1, v2, t0, t_coll, dt_coll, v1f, v2f = self.col_data
        sim_win = tk.Toplevel(self.root)
        sim_win.title("Simulation")
        default_t_end = min(t_coll + max(2.0, dt_coll * 0.8), t0 + 10.0)
        ctrl_frame = ttk.LabelFrame(sim_win, text="Simulation Control")
        ctrl_frame.pack(fill="x")
        ttk.Label(ctrl_frame, text=f"Impact Time t_coll = {t_coll:.2f}s | Impact Pos x_coll = {x1 + v1*(t_coll - t0):.2f}m").pack(side="left")
        f_inputs = ttk.Frame(ctrl_frame)
        f_inputs.pack(side="right")
        ttk.Label(f_inputs, text="Sim Start:").pack(side="left")
        e_sim_start = ttk.Entry(f_inputs, width=6)
        e_sim_start.insert(0, str(t0))
        e_sim_start.pack(side="left")
        ttk.Label(f_inputs, text="Sim End:").pack(side="left")
        e_sim_end = ttk.Entry(f_inputs, width=6)
        e_sim_end.insert(0, f"{default_t_end:.2f}")
        e_sim_end.pack(side="left")
        plot_frame = ttk.Frame(sim_win)
        plot_frame.pack(fill="both", expand=True)
        fig, ax = plt.subplots()
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        slider_frame = ttk.Frame(sim_win)
        slider_frame.pack(fill="x")
        lbl_time = ttk.Label(slider_frame, text=f"Time t = {t0:.2f}s")
        lbl_time.pack()
        slider = ttk.Scale(slider_frame, from_=t0, to=default_t_end, orient="horizontal")
        slider.pack(fill="x")
        ttk.Button(f_inputs, text="Apply", command=apply_col_sim_window).pack(side="left")
        slider.config(command=update_track_plot)
        apply_col_sim_window()
if _name_ == "_main_":
    root = tk.Tk()
    app = PAPSTApp(root)
    root.mainloop()
