# SOURCES:
# https://skepsis.nl/mainsite/inhoud/uploads/2022/05/Lazzarini.pdf
# https://clydekertzer.com/files/Buffon'sNeedleGoogleDoc.pdf 

import pygame
import numpy as np
import matplotlib.pyplot as plt
import sys

WIDTH, HEIGHT = 1200, 800
BG_COLOR = (15, 15, 25)
LINE_COLOR = (100, 100, 120)
NEEDLE_HIT_COLOR = (255, 50, 80)
NEEDLE_MISS_COLOR = (50, 255, 150)
TEXT_COLOR = (240, 240, 240)

D = 80.0
BATCH_NORMAL = 5000
BATCH_TURBO = 1_000_000

class BuffonSimulation:
    def __init__(self):
        self.total_needles = 0
        self.hit_needles = 0
        self.visual_needles = []
        self.pi_history = []
        self.n_history = []
        self.L = 0
        self.scenario_name = ""
        self.running = False
        self.limit = None
        self.turbo = False
        self.stop_on_accuracy = False
        self.finish_reason = ""

    def start_scenario(self, scenario_type):
        keep_turbo = self.turbo
        keep_stop = self.stop_on_accuracy
        self.__init__()
        self.turbo = keep_turbo
        self.stop_on_accuracy = keep_stop
        self.running = True
        
        if scenario_type == 'A':
            self.L = 0.5 * D
            self.scenario_name = "A: Short Needle (L=0.5D)"
            self.limit = None
        elif scenario_type == 'B':
            self.L = (5/6) * D
            self.scenario_name = "B: Lazzarini (L=0.83D)"
            self.limit = None
        elif scenario_type == 'C':
            self.L = (5/6) * D
            self.scenario_name = "C: Lazzarini Exact (N=3408)"
            self.limit = 3408
        elif scenario_type == 'D':
            self.L = 1.0 * D
            self.scenario_name = "D: Equal Length (L=D)"
            self.limit = None
        elif scenario_type == 'E':
            self.L = 1.5 * D
            self.scenario_name = "E: Long Needle (L=1.5D) [Break]"
            self.limit = None

    def run_math_batch(self, n_samples):
        dist_to_line = np.random.uniform(0, D/2.0, n_samples)
        theta = np.random.uniform(0, np.pi/2.0, n_samples)
        
        limit = (self.L / 2.0) * np.sin(theta)
        
        hits = np.sum(dist_to_line <= limit)
        
        self.total_needles += n_samples
        self.hit_needles += hits

    def generate_visuals(self):
        viz_count = 50
        cx = np.random.uniform(0, WIDTH, viz_count)
        cy = np.random.uniform(0, HEIGHT, viz_count)
        theta = np.random.uniform(0, np.pi, viz_count)
        
        x_proj = (self.L / 2) * np.cos(theta)
        y_proj = (self.L / 2) * np.sin(theta)
        
        x_start = cx - x_proj
        x_end = cx + x_proj
        y_start = cy - y_proj
        y_end = cy + y_proj
        
        hits_array = (x_start // D) != (x_end // D)
        
        self.visual_needles = []
        for i in range(viz_count):
            self.visual_needles.append((
                (x_start[i], y_start[i]), 
                (x_end[i], y_end[i]), 
                hits_array[i]
            ))

    def calculate_pi(self):
        if self.hit_needles == 0: return 0
        return (2 * self.L * self.total_needles) / (D * self.hit_needles)

    def update_plot_data(self):
        if self.total_needles > 0:
            current_pi = self.calculate_pi()
            self.pi_history.append(current_pi)
            self.n_history.append(self.total_needles)

plt.ion()
fig, ax = plt.subplots(figsize=(9, 5))
line_plot, = ax.plot([], [], 'c-', linewidth=1.5, label='Monte Carlo Pi')
ax.axhline(y=np.pi, color='r', linestyle='--', linewidth=2, label='True Pi')
ax.set_ylim(2.5, 4.0) 
ax.set_xlim(0, 1000000)
ax.set_xlabel('Total Samples')
ax.set_ylabel('Estimation')
ax.legend()
ax.grid(True, alpha=0.3)
fig.patch.set_facecolor('#1a1a2e')
ax.set_facecolor('#16213e')
ax.tick_params(colors='white')
ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')
for spine in ax.spines.values(): spine.set_color('white')

def update_matplotlib(sim):
    if not sim.n_history: return
    line_plot.set_xdata(sim.n_history)
    line_plot.set_ydata(sim.pi_history)
    
    if sim.total_needles > ax.get_xlim()[1]:
        ax.set_xlim(0, sim.total_needles * 1.1)
    
    pi_current = sim.pi_history[-1]
    
    if sim.L > D:
        ax.set_ylim(3.0, 4.0)
    else:
        err = abs(pi_current - np.pi)
        zoom = max(0.002, err * 2.5)
        ax.set_ylim(np.pi - zoom, np.pi + zoom)

    ax.set_title(f"{sim.scenario_name} | N={sim.total_needles:,}", color='white')
    fig.canvas.draw()
    fig.canvas.flush_events()

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Laborator 9: Final Project")
clock = pygame.time.Clock()
font = pygame.font.SysFont('Consolas', 18)
large_font = pygame.font.SysFont('Consolas', 36, bold=True)

sim = BuffonSimulation()

running_app = True
while running_app:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running_app = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                sim.start_scenario('A')
                sim.pi_history, sim.n_history = [], []
                line_plot.set_data([], [])
            if event.key == pygame.K_b:
                sim.start_scenario('B')
                sim.pi_history, sim.n_history = [], []
                line_plot.set_data([], [])
            if event.key == pygame.K_c:
                sim.start_scenario('C')
                sim.pi_history, sim.n_history = [], []
                line_plot.set_data([], [])
            if event.key == pygame.K_d:
                sim.start_scenario('D')
                sim.pi_history, sim.n_history = [], []
                line_plot.set_data([], [])
            if event.key == pygame.K_e:
                sim.start_scenario('E')
                sim.pi_history, sim.n_history = [], []
                line_plot.set_data([], [])
            if event.key == pygame.K_t:
                sim.turbo = not sim.turbo
            if event.key == pygame.K_s:
                sim.stop_on_accuracy = not sim.stop_on_accuracy

    if sim.running:
        current_batch_size = BATCH_TURBO if sim.turbo else BATCH_NORMAL
        
        actual_batch = current_batch_size
        
        if sim.limit is not None:
            remaining = sim.limit - sim.total_needles
            if remaining <= 0:
                sim.running = False
                sim.finish_reason = "LIMIT REACHED"
                actual_batch = 0
                sim.update_plot_data()
                update_matplotlib(sim)
            else:
                actual_batch = min(current_batch_size, remaining)

        if actual_batch > 0:
            sim.run_math_batch(actual_batch)
            sim.generate_visuals()
            
            pi_now = sim.calculate_pi()
            if sim.stop_on_accuracy and pi_now > 0:
                accuracy = (1 - abs(pi_now - np.pi) / np.pi) * 100
                if accuracy >= 99.999:
                    sim.running = False
                    sim.finish_reason = "ACCURACY TARGET REACHED!"
                    sim.update_plot_data()
                    update_matplotlib(sim)

            update_interval = BATCH_TURBO if sim.turbo else BATCH_NORMAL * 5
            
            if sim.running and (sim.total_needles % update_interval < actual_batch or sim.limit is not None):
                sim.update_plot_data()
                update_matplotlib(sim)

    screen.fill(BG_COLOR)
    
    for i in range(WIDTH // int(D) + 2):
        pygame.draw.line(screen, LINE_COLOR, (i*D, 0), (i*D, HEIGHT), 1)

    if sim.visual_needles: 
        for start, end, hit in sim.visual_needles:
            col = NEEDLE_HIT_COLOR if hit else NEEDLE_MISS_COLOR
            pygame.draw.line(screen, col, start, end, 2)

    pi_est = sim.calculate_pi()
    err = abs(pi_est - np.pi) if pi_est > 0 else 0
    accuracy = (1 - err/np.pi) * 100 if pi_est > 0 else 0
    
    speed_text = "TURBO" if sim.turbo else "NORMAL"
    speed_color = (255, 200, 0) if sim.turbo else (100, 200, 255)
    
    stop_text = "ON (>99.999%)" if sim.stop_on_accuracy else "OFF"
    stop_color = (0, 255, 0) if sim.stop_on_accuracy else (150, 150, 150)

    texts = [
        f"MODE: {sim.scenario_name}",
        f"SPEED:     {speed_text}",
        f"AUTO-STOP: {stop_text}",
        f"Samples:   {sim.total_needles:,.0f}" + (f" / {sim.limit}" if sim.limit else ""),
        f"Hits:      {sim.hit_needles:,.0f}",
        f"EST. PI:   {pi_est:.10f}",
        f"REAL PI:   {np.pi:.10f}",
        f"Accuracy:  {accuracy:.6f}%",
        "----------------",
        "KEYS: A, B, C, D, E",
        "KEY T: Toggle Speed",
        "KEY S: Toggle Auto-Stop"
    ]
    
    for i, t in enumerate(texts):
        col = TEXT_COLOR
        if "EST" in t: col = (0, 255, 100)
        if "Model Break" in sim.scenario_name and "EST" in t: col = (255, 50, 50)
        if "SPEED" in t: col = speed_color
        if "AUTO-STOP" in t: col = stop_color
        if "Accuracy" in t and accuracy >= 99.999: col = (255, 255, 0)
        
        screen.blit(font.render(t, True, col), (20, 20 + i*22))
        
    if not sim.running and sim.finish_reason:
        done_msg = large_font.render(sim.finish_reason, True, (255, 255, 0))
        screen.blit(done_msg, (WIDTH//2 - done_msg.get_width()//2, HEIGHT - 100))

    if not sim.running and sim.total_needles == 0:
        text = "SELECT SCENARIO (A(1/2) - B(Lazzarini 5/6) - C(3408 5/6) - D(1/1) - E(l>d))"
        words = text.split()
        lines = []
        current = ""
        max_width = WIDTH - 40
        for w in words:
            test = (current + " " + w).strip()
            if large_font.render(test, True, TEXT_COLOR).get_width() <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = w
        if current:
            lines.append(current)

        line_h = large_font.get_linesize()
        total_h = len(lines) * line_h
        y_start = HEIGHT // 2 - total_h // 2
        for i, line in enumerate(lines):
            msg = large_font.render(line, True, TEXT_COLOR)
            screen.blit(msg, (WIDTH//2 - msg.get_width()//2, y_start + i*line_h))

    pygame.display.flip()

pygame.quit()
plt.close()

if sim.total_needles > 0:
    print("\n" + "="*40)
    print("FINAL SIMULATION STATISTICS")
    print("="*40)
    print(f"Scenario:      {sim.scenario_name}")
    print(f"Stop Reason:   {sim.finish_reason if sim.finish_reason else 'Manual'}")
    print(f"Total Needles: {sim.total_needles:,}")
    print(f"Total Hits:    {sim.hit_needles:,}")
    pi_final = sim.calculate_pi()
    print(f"Estimated Pi:  {pi_final:.10f}")
    print(f"Real Pi:       {np.pi:.10f}")
    if sim.L > D:
        print("NOTE: Standard Pi formula invalid for L > D (Case E)")
    else:
        print(f"Accuracy %:    {(1 - abs(pi_final - np.pi)/np.pi)*100:.6f}%")
        print(f"Error:         {abs(pi_final - np.pi):.10f}")
    print("="*40 + "\n")
else:
    print("\nSimulation closed without running data.\n")

sys.exit()