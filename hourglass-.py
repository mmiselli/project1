import tkinter as tk
import random

class SimplePrettyHourglass:
    def __init__(self, master):
        self.master = master
        self.master.title("Гарний піщаний годинник")
        self.canvas = tk.Canvas(master, width=300, height=500, bg="#fdf6e3")
        self.canvas.pack()

        frame = tk.Frame(master)
        frame.pack()
        tk.Label(frame, text="Тривалість (сек):").pack(side=tk.LEFT)
        self.time_entry = tk.Entry(frame, width=5)
        self.time_entry.insert(0, "10")
        self.time_entry.pack(side=tk.LEFT)

        self.start_button = tk.Button(master, text="Старт", command=self.start)
        self.start_button.pack()

        self.flip_button = tk.Button(master, text="Перевернути", command=self.flip, state=tk.DISABLED)
        self.flip_button.pack()

        self.duration = 10
        self.interval = 100
        self.step = self.interval / 1000
        self.time = 0
        self.running = False
        self.flipped = False

        self.draw_outline()
        self.update_animation()

    def draw_outline(self):
        self.canvas.delete("all")
        self.canvas.create_polygon(80, 50, 220, 50, 150, 250, fill="#e0d4a8", outline="#8b7d5a")
        self.canvas.create_polygon(80, 450, 220, 450, 150, 250, fill="#e0d4a8", outline="#8b7d5a")

    def update_animation(self):
        self.canvas.delete("sand")

        ratio = min(self.time / self.duration, 1.0)
        top_height = 180 * (1 - ratio)
        bottom_height = 180 * ratio

        if not self.flipped:
            # Верхній пісок (вершиною вниз)
            self.canvas.create_polygon(
                90, 60, 210, 60, 150, 60 + top_height,
                fill="#d4af37", outline="", tags="sand"
            )
            # Нижній пісок (вершиною вгору)
            self.canvas.create_polygon(
                90, 450, 210, 450, 150, 450 - bottom_height,
                fill="#d4af37", outline="", tags="sand"
            )
            if self.running and self.time < self.duration:
                for _ in range(8):
                    x = 150 + random.uniform(-1.5, 1.5)
                    y1 = 60 + top_height
                    y2 = 450 - bottom_height
                    self.canvas.create_line(
                        x, y1, x + random.uniform(-1, 1), y2,
                        fill="#c2a300", width=1, tags="sand"
                    )
        else:
            # Верхній пісок (колишній низ, тепер вершиною вниз)
            self.canvas.create_polygon(
                90, 60, 210, 60, 150, 60 + bottom_height,
                fill="#d4af37", outline="", tags="sand"
            )
            # Нижній пісок (колишній верх, тепер вершиною вгору)
            self.canvas.create_polygon(
                90, 450, 210, 450, 150, 450 - top_height,
                fill="#d4af37", outline="", tags="sand"
            )
            if self.running and self.time < self.duration:
                for _ in range(8):
                    x = 150 + random.uniform(-1.5, 1.5)
                    y1 = 450 - top_height
                    y2 = 60 + bottom_height
                    self.canvas.create_line(
                        x, y1, x + random.uniform(-1, 1), y2,
                        fill="#c2a300", width=1, tags="sand"
                    )

        if self.running and self.time < self.duration:
            self.time += self.step
            self.master.after(self.interval, self.update_animation)
        else:
            self.running = False
            self.flip_button.config(state=tk.NORMAL)

    def start(self):
        try:
            self.duration = float(self.time_entry.get())
            if self.duration <= 0:
                raise ValueError
        except ValueError:
            self.duration = 10
            self.time_entry.delete(0, tk.END)
            self.time_entry.insert(0, "10")

        self.time = 0
        self.running = True
        self.flip_button.config(state=tk.DISABLED)
        self.draw_outline()
        self.update_animation()

    def flip(self):
        self.flipped = not self.flipped
        self.time = self.duration - self.time
        self.running = True
        self.flip_button.config(state=tk.DISABLED)
        self.draw_outline()
        self.update_animation()

if __name__ == "__main__":
    root = tk.Tk()
    app = SimplePrettyHourglass(root)
    root.mainloop()
