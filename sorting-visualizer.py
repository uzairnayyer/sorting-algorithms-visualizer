import tkinter as tk
from tkinter import ttk
import random
import time
import threading


class SortingVisualizer:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Sorting Algorithm Visualizer")
        self.window.geometry("1920x1080")
        self.window.configure(bg='#0a0a1a')
        self.window.resizable(True, True)
        
        self.array = []
        self.array_size = 50
        self.speed = 50
        self.sorting = False
        self.comparisons = 0
        self.swaps = 0
        self.start_time = 0
        
        self.colors = {
            'bar': '#00d4ff',
            'compare': '#ff4757',
            'swap': '#ffa502',
            'sorted': '#2ed573',
            'pivot': '#a55eea',
            'bg': '#0a0a1a',
            'panel': '#1e1e3f',
            'text': '#ffffff',
            'accent': '#00d4ff',
            'gradient1': '#667eea',
            'gradient2': '#764ba2'
        }

        self.setup_ui()
        self.generate_array()        
        self.window.bind('<Configure>', self.on_resize)
        self.window.mainloop()

    def setup_ui(self):
        main_container = tk.Frame(self.window, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        header_frame = tk.Frame(main_container, bg=self.colors['panel'], pady=20, padx=20)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        header_frame.configure(highlightbackground=self.colors['accent'], highlightthickness=2)
        
        title_label = tk.Label(header_frame, 
                               text="Sorting Algorithm Visualizer",
                               font=('Segoe UI', 24, 'bold'), 
                               bg=self.colors['panel'],
                               fg=self.colors['accent'])
        title_label.pack(pady=(0, 5))
        
        subtitle_label = tk.Label(header_frame, 
                                  text="Visualize how sorting algorithms work step by step",
                                  font=('Segoe UI', 11), 
                                  bg=self.colors['panel'],
                                  fg='#888888')
        subtitle_label.pack()
        
        control_panel = tk.Frame(main_container, bg=self.colors['panel'], pady=20, padx=20)
        control_panel.pack(fill=tk.X, pady=(0, 15))
        control_panel.configure(highlightbackground='#333366', highlightthickness=1)
        controls_row = tk.Frame(control_panel, bg=self.colors['panel'])
        controls_row.pack(fill=tk.X)

        algo_frame = tk.LabelFrame(controls_row, text="Algorithm", 
                                   bg=self.colors['panel'],
                                   fg=self.colors['accent'], 
                                   font=('Segoe UI', 11, 'bold'),
                                   padx=15, pady=10)
        algo_frame.pack(side=tk.LEFT, padx=10)

        self.algorithm_var = tk.StringVar(value="Bubble Sort")
        algorithms = ["Bubble Sort", "Selection Sort", "Insertion Sort"]

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Custom.TCombobox', 
                        fieldbackground='#2a2a5a',
                        background='#2a2a5a', 
                        foreground='white',
                        arrowcolor='white')
        style.map('Custom.TCombobox', 
                  fieldbackground=[('readonly', '#2a2a5a')],
                  selectbackground=[('readonly', '#3a3a7a')])

        self.algo_menu = ttk.Combobox(algo_frame, 
                                      textvariable=self.algorithm_var,
                                      values=algorithms, 
                                      state="readonly", 
                                      width=20,
                                      font=('Segoe UI', 11),
                                      style='Custom.TCombobox')
        self.algo_menu.pack(padx=5, pady=5)
        self.algo_menu.bind("<<ComboboxSelected>>", self.on_algorithm_change)

        size_frame = tk.LabelFrame(controls_row, text="Array Size", 
                                   bg=self.colors['panel'],
                                   fg=self.colors['accent'], 
                                   font=('Segoe UI', 11, 'bold'),
                                   padx=15, pady=10)
        size_frame.pack(side=tk.LEFT, padx=10)

        self.size_var = tk.IntVar(value=50)
        self.size_label = tk.Label(size_frame, text="50", 
                                   bg=self.colors['panel'], 
                                   fg='white',
                                   font=('Segoe UI', 12, 'bold'), width=4)
        self.size_label.pack()
        
        self.size_scale = tk.Scale(size_frame, from_=10, to=150, 
                                   orient=tk.HORIZONTAL,
                                   variable=self.size_var, 
                                   command=self.update_size,
                                   bg=self.colors['panel'], 
                                   fg=self.colors['text'],
                                   highlightthickness=0, 
                                   troughcolor='#2a2a5a',
                                   activebackground=self.colors['accent'], 
                                   length=150,
                                   showvalue=False,
                                   sliderlength=20)
        self.size_scale.pack(padx=5)
        
        speed_frame = tk.LabelFrame(controls_row, text="Speed", 
                                    bg=self.colors['panel'],
                                    fg=self.colors['accent'], 
                                    font=('Segoe UI', 11, 'bold'),
                                    padx=15, pady=10)
        speed_frame.pack(side=tk.LEFT, padx=10)

        self.speed_var = tk.IntVar(value=50)
        self.speed_label = tk.Label(speed_frame, text="50%", 
                                    bg=self.colors['panel'], 
                                    fg='white',
                                    font=('Segoe UI', 12, 'bold'), width=4)
        self.speed_label.pack()
        
        self.speed_scale = tk.Scale(speed_frame, from_=1, to=100, 
                                    orient=tk.HORIZONTAL,
                                    variable=self.speed_var, 
                                    command=self.update_speed,
                                    bg=self.colors['panel'], 
                                    fg=self.colors['text'],
                                    highlightthickness=0, 
                                    troughcolor='#2a2a5a',
                                    activebackground=self.colors['accent'], 
                                    length=150,
                                    showvalue=False,
                                    sliderlength=20)
        self.speed_scale.pack(padx=5)
      
        btn_frame = tk.Frame(controls_row, bg=self.colors['panel'])
        btn_frame.pack(side=tk.RIGHT, padx=20)
        
        self.generate_btn = tk.Button(btn_frame, text="Generate New Array",
                                      command=self.generate_array,
                                      bg='#e74c3c', fg='white', 
                                      font=('Segoe UI', 11, 'bold'),
                                      padx=20, pady=12, 
                                      cursor='hand2', 
                                      relief=tk.FLAT,
                                      activebackground='#c0392b',
                                      activeforeground='white')
        self.generate_btn.pack(side=tk.LEFT, padx=8)
        self.add_button_hover(self.generate_btn, '#e74c3c', '#c0392b')
        
        self.sort_btn = tk.Button(btn_frame, text="Start Sorting",
                                  command=self.start_sort,
                                  bg='#00d4ff', fg='#0a0a1a', 
                                  font=('Segoe UI', 11, 'bold'),
                                  padx=20, pady=12, 
                                  cursor='hand2', 
                                  relief=tk.FLAT,
                                  activebackground='#00a8cc',
                                  activeforeground='#0a0a1a')
        self.sort_btn.pack(side=tk.LEFT, padx=8)
        self.add_button_hover(self.sort_btn, '#00d4ff', '#00a8cc')

        self.stop_btn = tk.Button(btn_frame, text="Stop",
                                  command=self.stop_sort,
                                  bg='#ff6b6b', fg='white', 
                                  font=('Segoe UI', 11, 'bold'),
                                  padx=20, pady=12, 
                                  cursor='hand2', 
                                  relief=tk.FLAT,
                                  activebackground='#ee5a5a', 
                                  state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=8)
        
        stats_panel = tk.Frame(main_container, bg=self.colors['panel'], pady=15)
        stats_panel.pack(fill=tk.X, pady=(0, 15))
        stats_panel.configure(highlightbackground='#333366', highlightthickness=1)
        stats_container = tk.Frame(stats_panel, bg=self.colors['panel'])
        stats_container.pack()

        comp_frame = tk.Frame(stats_container, bg='#2a2a5a', padx=20, pady=10)
        comp_frame.pack(side=tk.LEFT, padx=15)
        tk.Label(comp_frame, text="Comparisons", bg='#2a2a5a', fg='#888888',
                 font=('Segoe UI', 10)).pack()
        self.comparisons_label = tk.Label(comp_frame, text="0",
                                          bg='#2a2a5a', fg='#ff4757',
                                          font=('Segoe UI', 20, 'bold'))
        self.comparisons_label.pack()
        
        swap_frame = tk.Frame(stats_container, bg='#2a2a5a', padx=20, pady=10)
        swap_frame.pack(side=tk.LEFT, padx=15)
        tk.Label(swap_frame, text="Swaps", bg='#2a2a5a', fg='#888888',
                 font=('Segoe UI', 10)).pack()
        self.swaps_label = tk.Label(swap_frame, text="0",
                                    bg='#2a2a5a', fg='#ffa502',
                                    font=('Segoe UI', 20, 'bold'))
        self.swaps_label.pack()

        time_frame = tk.Frame(stats_container, bg='#2a2a5a', padx=20, pady=10)
        time_frame.pack(side=tk.LEFT, padx=15)
        tk.Label(time_frame, text="Time", bg='#2a2a5a', fg='#888888',
                 font=('Segoe UI', 10)).pack()
        self.time_label = tk.Label(time_frame, text="0.000s",
                                   bg='#2a2a5a', fg='#2ed573',
                                   font=('Segoe UI', 20, 'bold'))
        self.time_label.pack()
        
        complexity_frame = tk.Frame(stats_container, bg='#2a2a5a', padx=20, pady=10)
        complexity_frame.pack(side=tk.LEFT, padx=15)
        tk.Label(complexity_frame, text="📈 Time Complexity", bg='#2a2a5a', fg='#888888',
                 font=('Segoe UI', 10)).pack()
        self.complexity_label = tk.Label(complexity_frame, text="O(n²)",
                                         bg='#2a2a5a', fg=self.colors['accent'],
                                         font=('Segoe UI', 20, 'bold'))
        self.complexity_label.pack()
        
        canvas_frame = tk.Frame(main_container, bg=self.colors['panel'], padx=15, pady=15)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        canvas_frame.configure(highlightbackground='#333366', highlightthickness=1)

        self.canvas = tk.Canvas(canvas_frame, bg='#12122a', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        legend_frame = tk.Frame(main_container, bg=self.colors['panel'], pady=12)
        legend_frame.pack(fill=tk.X, pady=(15, 0))
        legend_frame.configure(highlightbackground='#333366', highlightthickness=1)

        legend_title = tk.Label(legend_frame, text="Color Legend:", 
                                bg=self.colors['panel'], fg=self.colors['text'],
                                font=('Segoe UI', 11, 'bold'))
        legend_title.pack(side=tk.LEFT, padx=20)

        legends = [
            ("Normal", self.colors['bar'], "🔵"),
            ("Comparing", self.colors['compare'], "🔴"),
            ("Swapping", self.colors['swap'], "🟡"),
            ("Sorted", self.colors['sorted'], "🟢"),
            ("Pivot", self.colors['pivot'], "🟢"),
        ]

        for text, color, emoji in legends:
            leg_item = tk.Frame(legend_frame, bg=self.colors['panel'])
            leg_item.pack(side=tk.LEFT, padx=20)

            color_box = tk.Canvas(leg_item, width=25, height=25, bg=color, 
                                  highlightthickness=2, highlightbackground='white')
            color_box.pack(side=tk.LEFT, padx=5)

            tk.Label(leg_item, text=f"{emoji} {text}", 
                     bg=self.colors['panel'], fg=self.colors['text'],
                     font=('Segoe UI', 10, 'bold')).pack(side=tk.LEFT)

    def add_button_hover(self, button, normal_color, hover_color):
        def on_enter(e):
            button['background'] = hover_color
        def on_leave(e):
            button['background'] = normal_color
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def on_resize(self, event=None):
        if not self.sorting and self.array:
            self.draw_array()

    def on_algorithm_change(self, event=None):
        complexities = {
            "Bubble Sort": "O(n²)",
            "Selection Sort": "O(n²)",
            "Insertion Sort": "O(n²)"
        }
        algo = self.algorithm_var.get()
        self.complexity_label.config(text=complexities.get(algo, 'O(n²)'))

    def update_size(self, val):
        if not self.sorting:
            self.array_size = int(val)
            self.size_label.config(text=str(self.array_size))
            self.generate_array()

    def update_speed(self, val):
        self.speed = int(val)
        self.speed_label.config(text=f"{self.speed}%")

    def generate_array(self):
        if self.sorting:
            return

        self.array = [random.randint(10, 500) for _ in range(self.array_size)]
        self.comparisons = 0
        self.swaps = 0
        self.update_stats()
        self.draw_array()

    def draw_array(self, color_positions=None):
        self.canvas.delete("all")

        if not self.array:
            return

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width <= 1:
            canvas_width = 1100
        if canvas_height <= 1:
            canvas_height = 400

        padding = 20
        bar_width = (canvas_width - 2 * padding) / len(self.array)
        max_val = max(self.array)
        
        
        for i, val in enumerate(self.array):
            x0 = padding + i * bar_width
            y0 = canvas_height - padding
            x1 = x0 + bar_width - 2
            bar_height = (val / max_val) * (canvas_height - 2 * padding - 20)
            y1 = y0 - bar_height

            if color_positions and i in color_positions:
                color = color_positions[i]
            else:
                color = self.colors['bar']

            
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline='', width=0)
            
            highlight_height = min(5, bar_height * 0.1)
            self.canvas.create_rectangle(x0, y1, x1, y1 + highlight_height, 
                                         fill=self.lighten_color(color), outline='')
           
            if bar_width > 30:
                self.canvas.create_text((x0 + x1) / 2, y1 - 12, text=str(val),
                                        fill='white', font=('Segoe UI', 8, 'bold'))

        self.window.update_idletasks()

    def lighten_color(self, hex_color):        
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        
        factor = 1.3
        r = min(255, int(r * factor))
        g = min(255, int(g * factor))
        b = min(255, int(b * factor))
        
        return f'#{r:02x}{g:02x}{b:02x}'

    def update_stats(self):
        elapsed = time.time() - self.start_time if self.start_time else 0
        self.comparisons_label.config(text=str(self.comparisons))
        self.swaps_label.config(text=str(self.swaps))
        self.time_label.config(text=f"{elapsed:.3f}s")

    def get_delay(self):
        return (101 - self.speed) / 1000

    def start_sort(self):
        if self.sorting:
            return

        self.sorting = True
        self.comparisons = 0
        self.swaps = 0
        self.start_time = time.time()
        
        self.sort_btn.config(state=tk.DISABLED)
        self.generate_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.size_scale.config(state=tk.DISABLED)
        self.algo_menu.config(state=tk.DISABLED)

        algo = self.algorithm_var.get()
        sort_thread = threading.Thread(target=self.run_sort, args=(algo,), daemon=True)
        sort_thread.start()

    def stop_sort(self):
        self.sorting = False

    def run_sort(self, algorithm):
        try:
            if algorithm == "Bubble Sort":
                self.bubble_sort()
            elif algorithm == "Selection Sort":
                self.selection_sort()
            elif algorithm == "Insertion Sort":
                self.insertion_sort()

            if self.sorting:
                self.show_sorted_animation()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.finish_sort()

    def finish_sort(self):
        self.sorting = False
        self.sort_btn.config(state=tk.NORMAL)
        self.generate_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.size_scale.config(state=tk.NORMAL)
        self.algo_menu.config(state='readonly')

    def show_sorted_animation(self):
        for i in range(len(self.array)):
            if not self.sorting:
                break
            color_positions = {j: self.colors['sorted'] for j in range(i + 1)}
            self.draw_array(color_positions)
            time.sleep(0.02)

        self.draw_array({i: self.colors['sorted'] for i in range(len(self.array))})

    def bubble_sort(self):
        n = len(self.array)
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                if not self.sorting:
                    return

                self.comparisons += 1
                self.draw_array({j: self.colors['compare'], j + 1: self.colors['compare']})
                time.sleep(self.get_delay())

                if self.array[j] > self.array[j + 1]:
                    self.array[j], self.array[j + 1] = self.array[j + 1], self.array[j]
                    self.swaps += 1
                    swapped = True
                    
                    self.draw_array({j: self.colors['swap'], j + 1: self.colors['swap']})
                    time.sleep(self.get_delay())

                self.update_stats()
            if not swapped:
                break

    def selection_sort(self):
        n = len(self.array)
        for i in range(n):
            min_idx = i
            
            for j in range(i + 1, n):
                if not self.sorting:
                    return

                self.comparisons += 1
                
                sorted_colors = {k: self.colors['sorted'] for k in range(i)}
                sorted_colors[min_idx] = self.colors['pivot']
                sorted_colors[j] = self.colors['compare']
                self.draw_array(sorted_colors)
                time.sleep(self.get_delay())

                if self.array[j] < self.array[min_idx]:
                    min_idx = j

                self.update_stats()

            if min_idx != i:
                self.array[i], self.array[min_idx] = self.array[min_idx], self.array[i]
                self.swaps += 1
                sorted_colors = {k: self.colors['sorted'] for k in range(i)}
                sorted_colors[i] = self.colors['swap']
                sorted_colors[min_idx] = self.colors['swap']
                self.draw_array(sorted_colors)
                time.sleep(self.get_delay())

    def insertion_sort(self):
        for i in range(1, len(self.array)):
            key = self.array[i]
            j = i - 1

            sorted_colors = {k: self.colors['sorted'] for k in range(i)}
            sorted_colors[i] = self.colors['pivot']
            self.draw_array(sorted_colors)
            time.sleep(self.get_delay())

            while j >= 0 and self.array[j] > key:
                if not self.sorting:
                    return

                self.comparisons += 1
                self.array[j + 1] = self.array[j]
                self.swaps += 1

                sorted_colors = {k: self.colors['sorted'] for k in range(j)}
                sorted_colors[j] = self.colors['compare']
                sorted_colors[j + 1] = self.colors['swap']
                self.draw_array(sorted_colors)
                time.sleep(self.get_delay())

                j -= 1
                self.update_stats()
            
            self.array[j + 1] = key
            self.comparisons += 1  
            self.update_stats()

if __name__ == "__main__":
    app = SortingVisualizer()
