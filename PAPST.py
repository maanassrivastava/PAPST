import math
import tkinter as tk
from tkinter import messagebox, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
INFO_DB = {
    "pos": ("Final Position & Displacement", "Position vector locates the particle at time t_f. Displacement vector represents the straight-line change from initial to final position.", "r_f = r_0 + v_0·Δt + ½·a·(Δt)² | Δr = r_f - r_0", "Displacement is like drawing a straight arrow from start to finish on a map, regardless of the path taken."),
    "vel": ("Velocity & Average Velocity", "Final velocity is instantaneous speed and direction at t_f. Average velocity is total displacement divided by total elapsed time.", "v_f = v_0 + a·Δt | v_avg = Δr / Δt = ½(v_0 + v_f)", "Your speedometer shows instantaneous velocity, while your total trip distance divided by time gives average velocity."),
    "acc": ("Acceleration", "Rate of change of velocity over time. In this module, acceleration is treated as constant.", "a_f = a_0 = Constant", "Pushing down on the gas pedal at a steady rate provides constant acceleration."),
    "force": ("Net Force", "The overall vector force acting on the particle, derived from Newton's Second Law.", "F_net = m · a", "How hard you need to push a object to accelerate it—heavier objects require proportionally more force."),
    "impulse": ("Impulse", "The cumulative effect of a force acting over time, which equals the total change in linear momentum.", "J = F_net · Δt = Δp = m · (v_f - v_0)", "Follow-through in sports like tennis or golf increases impulse by extending contact time with the ball."),
    "momentum": ("Net Linear Momentum", "Quantity of motion possessed by the particle due to its mass and final velocity.", "p = m · v_f", "A heavy freight train at 10 km/h has vastly more momentum than a cricket ball at 100 km/h because of its mass."),
    "ke": ("Kinetic Energy (Initial & Final)", "Scalar mechanical energy possessed by the particle due to its speed.", "KE_i = ½·m·|v_0|² | KE_f = ½·m·|v_f|²", "Speeding up from 20 km/h to 40 km/h requires 4x more kinetic energy because energy scales with velocity squared."),
    "work": ("Work Done (Change in KE)", "Energy transferred to or from the particle by the net force, governed by the Work-Energy Theorem.", "W = ΔKE = KE_f - KE_i = F_net · Δr", "Pushing a stalled car forwards does positive work, increasing its kinetic energy."),
    "power": ("Power (Final & Average)", "Rate at which work is performed or energy is transferred per unit time.", "P_f = F_net · v_f | P_avg = W / Δt", "A high-horsepower sports car transfers the same energy as a economy car, but does it in a fraction of the time."),
    "collision": ("1D Particle Collision & Restitution", "Conservation of linear momentum applies to all isolated collisions. The coefficient of restitution (e) measures elasticity.", "v1f = [(m1 - e·m2)v1i + m2(1+e)v2i] / (m1 + m2)\nv2f = [m1(1+e)v1i + (m2 - e·m1)v2i] / (m1 + m2)", "e = 1 means perfectly elastic (billiard balls, no KE lost); e = 0 means perfectly inelastic (two lumps of clay sticking together).")
}
def show_info(concept_key):
    if concept_key not in INFO_DB: return
    name, defn, formula, analogy = INFO_DB[concept_key]
    win = tk.Toplevel()
    win.title(f"Concept Info: {name}")
    ttk.Label(win, text=name).pack()
    ttk.Label(win, text=f"Definition:\n{defn}\n\nFormula:\n{formula}\n\nAnalogy:\n{analogy}", wraplength=400, justify="left").pack()
    ttk.Button(win, text="Close", command=win.destroy).pack()
class PAPSTApp:
    def __init__(self, root):
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
    def parse_inputs(self):
        dim = self.current_dim
        r0 = np.array([float(self.entries["r0"][i].get()) for i in range(dim)])
        v0 = np.array([float(self.entries["v0"][i].get()) for i in range(dim)])
        a0 = np.array([float(self.entries["a0"][i].get()) for i in range(dim)])
        t0 = float(self.entries["t0"].get())
        tf = float(self.entries["tf"].get())
        m_str = self.entries["m"].get().strip()
        if not m_str: raise ValueError("Please input the mass m.")
        m = float(m_str)
        if m <= 0: raise ValueError("Mass m must be positive.")
        if tf <= t0: raise ValueError("Final time t_f can not be smaller than t₀.")
        return r0, v0, a0, t0, tf, m
    def calculate_kinematics(self):
        try:
            r0, v0, a0, t0, tf, m = self.parse_inputs()
            dt = tf - t0
            rf = r0 + v0 * dt + 0.5 * a0 * (dt**2)
            disp = rf - r0
            vf = v0 + a0 * dt
            v_avg = disp / dt
            af = a0
            F_net = m * af
            impulse = F_net * dt
            p_net = m * vf
            ke_i = 0.5 * m * np.sum(v0**2)
            ke_f = 0.5 * m * np.sum(vf**2)
            work = ke_f - ke_i
            p_f = np.dot(F_net, vf)
            p_avg = work / dt
            def fmt_vec(v, unit):
                if self.current_dim == 1: return f"{v[0]:.2f} {unit}"
                elif self.current_dim == 2: return f"({v[0]:.2f}, {v[1]:.2f}) {unit}"
                else: return f"({v[0]:.2f}, {v[1]:.2f}, {v[2]:.2f}) {unit}"
            self.out_labels["pos_1"].config(text=f"Final Position (r_f): {fmt_vec(rf, 'm')}")
            self.out_labels["pos_2"].config(text=f"Displacement (Δr):    {fmt_vec(disp, 'm')}")
            self.out_labels["vel_1"].config(text=f"Final Velocity (v_f): {fmt_vec(vf, 'm/s')}")
            self.out_labels["vel_2"].config(text=f"Average Velocity (v_avg): {fmt_vec(v_avg, 'm/s')}")
            self.out_labels["acc_1"].config(text=f"Final Acceleration (a_f): {fmt_vec(af, 'm/s²')}")
            self.out_labels["force_1"].config(text=f"Net Force (F_net):    {fmt_vec(F_net, 'N')}")
            self.out_labels["impulse_1"].config(text=f"Impulse (J):          {fmt_vec(impulse, 'N·s')}")
            self.out_labels["momentum_1"].config(text=f"Net Linear Momentum:  {fmt_vec(p_net, 'kg·m/s')}")
            self.out_labels["ke_1"].config(text=f"Initial KE (KE_i):    {ke_i:.2f} J")
            self.out_labels["ke_2"].config(text=f"Final KE (KE_f):      {ke_f:.2f} J")
            self.out_labels["work_1"].config(text=f"Work Done (W):        {work:.2f} J")
            self.out_labels["power_1"].config(text=f"Final Power (P_f):    {p_f:.2f} W")
            self.out_labels["power_2"].config(text=f"Average Power (P_avg): {p_avg:.2f} W")
            self.btn_sim.config(state="normal")
            self.calc_data = (r0, v0, a0, t0, tf)
        except ValueError as e: messagebox.showerror("Error", str(e))
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
    def calculate_collision(self):
        try:
            m1_str, m2_str = self.col_entries["m1"].get().strip(), self.col_entries["m2"].get().strip()
            if not m1_str or not m2_str: raise ValueError("Mass (m₁ and m₂) are required.")
            m1, m2 = float(m1_str), float(m2_str)
            x1, x2 = float(self.col_entries["x1"].get()), float(self.col_entries["x2"].get())
            v1, v2 = float(self.col_entries["v1"].get()), float(self.col_entries["v2"].get())
            t0, e = float(self.col_entries["t0"].get()), float(self.col_entries["e"].get())
            if m1 <= 0 or m2 <= 0: raise ValueError("Masses must be positive.")
            if not (0.0 <= e <= 1.0): raise ValueError("Coefficient of restitution (e) must lie between 0 and 1.")
            rel_v, rel_x = v1 - v2, x2 - x1
            if rel_x == 0: raise ValueError("Particles are already at the same position")
            if (rel_x > 0 and rel_v <= 0) or (rel_x < 0 and rel_v >= 0): raise ValueError(f"No Collision")
            dt_coll = rel_x / rel_v
            t_coll = t0 + dt_coll
            x_coll = x1 + v1 * dt_coll
            v1f = ((m1 - e * m2) * v1 + m2 * (1 + e) * v2) / (m1 + m2)
            v2f = (m1 * (1 + e) * v1 + (m2 - e * m1) * v2) / (m1 + m2)
            ke_i = 0.5 * m1 * (v1**2) + 0.5 * m2 * (v2**2)
            ke_f = 0.5 * m1 * (v1f**2) + 0.5 * m2 * (v2f**2)
            ke_loss = ke_i - ke_f
            self.col_out_labels["t_dt_1"].config(text=f"Time for Collision (Δt_coll): {dt_coll:.2f} s")
            self.col_out_labels["t_dt_2"].config(text=f"Time of Collision (t_coll):  {t_coll:.2f} s")
            self.col_out_labels["pos_1"].config(text=f"Position at Collision (x_coll): {x_coll:.2f} m")
            self.col_out_labels["v1f_1"].config(text=f"Particle 1 Final Vel (v1f): {v1f:.2f} m/s")
            self.col_out_labels["v2f_1"].config(text=f"Particle 2 Final Vel (v2f): {v2f:.2f} m/s")
            self.col_out_labels["ke_1"].config(text=f"Initial System KE (KE_i):   {ke_i:.2f} J")
            self.col_out_labels["ke_2"].config(text=f"Final System KE (KE_f):     {ke_f:.2f} J")
            self.col_out_labels["loss_1"].config(text=f"Kinetic Energy Lost (ΔKE):  {ke_loss:.2f} J")
            self.btn_col_sim.config(state="normal")
            self.col_data = (m1, m2, x1, x2, v1, v2, t0, t_coll, dt_coll, v1f, v2f)
        except ValueError as err: messagebox.showerror("Error", str(err))
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
        def update_plot(val):
            try:
                t_sim_s, t_sim_e = float(e_sim_start.get()), float(e_sim_end.get())
                if not (t0 <= t_sim_s < t_sim_e <= tf) or (t_sim_e - t_sim_s) > 10.0: return
                t_curr = float(val)
                if t_curr < t_sim_s: t_curr = t_sim_s
                if t_curr > t_sim_e: t_curr = t_sim_e
                lbl_time.config(text=f"Time t = {t_curr:.2f} s")
                fig.clear()
                t_arr = np.linspace(t_sim_s, t_sim_e, 200)
                if self.current_dim == 1:
                    ax = fig.add_subplot(111)
                    x_arr = r0[0] + v0[0] * t_arr + 0.5 * a0[0] * (t_arr**2)
                    x_curr = r0[0] + v0[0] * t_curr + 0.5 * a0[0] * (t_curr**2)
                    ax.plot(t_arr, x_arr, color="blue", label="Position x(t)")
                    ax.scatter([t_curr], [x_curr], color="red", s=60, zorder=5, label=f"t = {t_curr:.2f}s")
                    ax.set_xlabel("Time (s)")
                    ax.set_ylabel("X Position (m)")
                    ax.set_title("Simulation")
                    ax.grid(True)
                    ax.legend()
                elif self.current_dim == 2:
                    ax = fig.add_subplot(111)
                    x_arr = r0[0] + v0[0] * t_arr + 0.5 * a0[0] * (t_arr**2)
                    y_arr = r0[1] + v0[1] * t_arr + 0.5 * a0[1] * (t_arr**2)
                    x_curr = r0[0] + v0[0] * t_curr + 0.5 * a0[0] * (t_curr**2)
                    y_curr = r0[1] + v0[1] * t_curr + 0.5 * a0[1] * (t_curr**2)
                    ax.plot(x_arr, y_arr, color="blue", label="Path Trajectory")
                    ax.scatter([x_curr], [y_curr], color="red", s=60, zorder=5, label=f"Pos at t={t_curr:.2f}s")
                    ax.set_xlabel("X Position (m)")
                    ax.set_ylabel("Y Position (m)")
                    ax.set_title("Simulation")
                    ax.grid(True)
                    ax.legend()
                else:
                    ax = fig.add_subplot(111, projection="3d")
                    x_arr = r0[0] + v0[0] * t_arr + 0.5 * a0[0] * (t_arr**2)
                    y_arr = r0[1] + v0[1] * t_arr + 0.5 * a0[1] * (t_arr**2)
                    z_arr = r0[2] + v0[2] * t_arr + 0.5 * a0[2] * (t_arr**2)
                    x_curr = r0[0] + v0[0] * t_curr + 0.5 * a0[0] * (t_curr**2)
                    y_curr = r0[1] + v0[1] * t_curr + 0.5 * a0[1] * (t_curr**2)
                    z_curr = r0[2] + v0[2] * t_curr + 0.5 * a0[2] * (t_curr**2)
                    ax.plot(x_arr, y_arr, z_arr, color="purple", label="3D Path")
                    ax.scatter([x_curr], [y_curr], [z_curr], color="red", s=60, zorder=5, label=f"Pos at t={t_curr:.2f}s")
                    ax.set_xlabel("X (m)")
                    ax.set_ylabel("Y (m)")
                    ax.set_zlabel("Z (m)")
                    ax.set_title("Simulation")
                    ax.legend()
                canvas.draw()
            except Exception: pass
        def apply_sim_window():
            try:
                t_sim_s, t_sim_e = float(e_sim_start.get()), float(e_sim_end.get())
                if not (t0 <= t_sim_s < t_sim_e <= tf):
                    messagebox.showerror("Window Error", f"Simulation window [{t_sim_s}, {t_sim_e}] must be within calculated bounds [{t0}, {tf}].")
                    return
                if (t_sim_e - t_sim_s) > 10.0:
                    messagebox.showerror("Window Error", "Simulation duration cannot exceed 10 seconds at a time.")
                    return
                slider.config(from_=t_sim_s, to=t_sim_e)
                slider.set(t_sim_s)
                update_plot(t_sim_s)
            except ValueError: messagebox.showerror("Input Error", "Please enter valid numbers for time range.")
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
        t_0_val = t0
        def update_track_plot(val):
            try:
                t_sim_s, t_sim_e = float(e_sim_start.get()), float(e_sim_end.get())
                t_curr = float(val)
                if t_curr < t_sim_s: t_curr = t_sim_s
                if t_curr > t_sim_e: t_curr = t_sim_e
                lbl_time.config(text=f"Time t = {t_curr:.2f} s")
                if t_curr <= t_coll: pos1, pos2 = x1 + v1 * (t_curr - t_0_val), x2 + v2 * (t_curr - t_0_val)
                else:
                    x_coll = x1 + v1 * (t_coll - t_0_val)
                    pos1, pos2 = x_coll + v1f * (t_curr - t_coll), x_coll + v2f * (t_curr - t_coll)
                ax.clear()
                all_t = np.linspace(t_sim_s, t_sim_e, 50)
                p1_all = np.where(all_t <= t_coll, x1 + v1 * (all_t - t_0_val), (x1 + v1 * (t_coll - t_0_val)) + v1f * (all_t - t_coll))
                p2_all = np.where(all_t <= t_coll, x2 + v2 * (all_t - t_0_val), (x1 + v1 * (t_coll - t_0_val)) + v2f * (all_t - t_coll))
                x_min, x_max = min(np.min(p1_all), np.min(p2_all)) - 2.0, max(np.max(p1_all), np.max(p2_all)) + 2.0
                ax.axhline(0, color="gray", linewidth=2, linestyle="--")
                x_impact = x1 + v1 * (t_coll - t_0_val)
                ax.axvline(x=x_impact, color="red", linestyle=":", alpha=0.6, label=f"Impact Point ({x_impact:.1f} m)")
                ax.scatter([pos1], [0], color="blue", s=250, zorder=5, label=f"P1 (m1={m1}kg) @ {pos1:.2f}m")
                ax.scatter([pos2], [0], color="green", s=250, zorder=5, label=f"P2 (m2={m2}kg) @ {pos2:.2f}m")
                v1_curr = v1 if t_curr <= t_coll else v1f
                v2_curr = v2 if t_curr <= t_coll else v2f
                ax.quiver(pos1, 0, v1_curr, 0, angles="xy", scale_units="xy", scale=1, color="blue", width=0.008, headwidth=4)
                ax.quiver(pos2, 0, v2_curr, 0, angles="xy", scale_units="xy", scale=1, color="green", width=0.008, headwidth=4)
                ax.set_xlim(x_min, x_max)
                ax.set_ylim(-1, 1)
                ax.set_yticks([])
                ax.set_xlabel("1D Track Position X (m)")
                ax.set_title("1D Collision Simulation")
                ax.grid(True, axis="x")
                ax.legend(loc="upper right")
                canvas.draw()
            except Exception: pass
        def apply_col_sim_window():
            try:
                t_sim_s, t_sim_e = float(e_sim_start.get()), float(e_sim_end.get())
                if t_sim_s >= t_sim_e:
                    messagebox.showerror("Window Error", "Sim Start must be less than Sim End.")
                    return
                if (t_sim_e - t_sim_s) > 10.0:
                    messagebox.showerror("Window Error", "Simulation window cannot exceed 10 seconds at a time.")
                    return
                slider.config(from_=t_sim_s, to=t_sim_e)
                slider.set(t_sim_s)
                update_track_plot(t_sim_s)
            except ValueError: messagebox.showerror("Input Error", "Please enter valid numbers for time range.")
        ttk.Button(f_inputs, text="Apply", command=apply_col_sim_window).pack(side="left")
        slider.config(command=update_track_plot)
        apply_col_sim_window()
if __name__ == "__main__":
    root = tk.Tk()
    app = PAPSTApp(root)
    root.mainloop()
