import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class EvaluationVisualizer:
    def __init__(self, root):
        self.root = root
        self.metrics_history = {
            'rouge1': [],
            'rouge2': [],
            'rougeL': [],
            'bleu': [],
            'meteor': [],
            'bert_f1': []
        }
        # Define typical ranges for each metric based on literature
        self.metric_ranges = {
            'rouge1': (0.0, 0.5),
            'rouge2': (0.0, 0.45),
            'rougeL': (0.0, 0.48),
            'bleu': (0.0, 0.5),
            'meteor': (0.0, 0.35),
            'bert_f1': (0.0, 0.8)
        }
        self.setup_plots()
        
    def normalize_score(self, metric, value):
        # Normalization formula
        min_val, max_val = self.metric_ranges[metric]
        normalized = (value - min_val) / (max_val - min_val)
        return max(0, min(1, normalized))
    
    def setup_plots(self):
        # Create frames for plots
        self.plot_frame = tk.Frame(self.root, bg="white")
        self.plot_frame.grid(row=6, column=0, columnspan=3, sticky="nsew", padx=20, pady=10)
        self.plot_frame.grid_remove()  # Hide initially
        
        # Progress plot
        self.fig_progress = Figure(figsize=(8, 4))
        self.ax_progress = self.fig_progress.add_subplot(111)
        self.fig_progress.patch.set_facecolor('#FFFFFF')
        self.ax_progress.set_facecolor('#F8F9FA')
        
        # Create canvas for progress plot
        self.canvas_progress = FigureCanvasTkAgg(self.fig_progress, master=self.plot_frame)
        self.canvas_progress_widget = self.canvas_progress.get_tk_widget()
        self.canvas_progress_widget.pack(fill=tk.BOTH, expand=True)
        
        # Setup radar chart
        self.final_frame = tk.Frame(self.root, bg="white")
        self.final_frame.grid(row=7, column=0, columnspan=3, sticky="nsew", padx=20, pady=10)
        self.final_frame.grid_remove()
        self.fig_radar = Figure(figsize=(3, 3))  # Smaller size
        self.ax_radar = self.fig_radar.add_subplot(111, projection='polar')
        self.canvas_radar = FigureCanvasTkAgg(self.fig_radar, master=self.final_frame)
        self.canvas_radar_widget = self.canvas_radar.get_tk_widget()
        self.canvas_radar_widget.pack(fill=tk.BOTH, expand=True)
        
    def show_plots(self):
        self.plot_frame.grid()
        
    def hide_plots(self):
        self.plot_frame.grid_remove()
        self.final_frame.grid_remove()
        
    def update_plots(self, metrics):
        # Update metrics for every new sample
        for metric, value in metrics.items():
            if metric in self.metrics_history:
                self.metrics_history[metric].append(value if value is not None else 0.0)
        
        # Only show and update plot if we have at least 1 sample
        if len(next(iter(self.metrics_history.values()))) >= 1:
            self.show_plots()
            # Clear previous plot
            self.ax_progress.clear()
            
            # Get data for bars
            n_samples = len(next(iter(self.metrics_history.values())))
            metrics = list(self.metrics_history.keys())
            colors = ['#4E79A7', '#F28E2B', '#E15759', '#76B7B2', '#59A14F', '#EDC948']
            
            # Calculate bar positions
            n_metrics = len(metrics)
            bar_width = 0.8 / n_metrics  # Width of each bar
            # Plot normalized bars for each metric
            for idx, (metric, color) in enumerate(zip(metrics, colors)):
                # Calculate bar positions - centered within each sample position
                positions = np.arange(n_samples) + (idx - n_metrics/2 + 0.5) * bar_width
                
                # Explicitly handle zero values
                raw_values = [v if v is not None else 0.0 for v in self.metrics_history[metric]]
                norm_values = [self.normalize_score(metric, v) for v in raw_values]
                # Plot bars
                self.ax_progress.bar(positions, norm_values, bar_width, 
                                   label=f'{metric} (norm)', 
                                   color=color, alpha=0.8, 
                                   edgecolor='black', linewidth=1)
            
            self.ax_progress.set_title('Normalized Metrics Progress', pad=15, fontsize=10, fontweight='bold')
            self.ax_progress.set_xlabel('Samples Processed', labelpad=10, fontsize=8)
            self.ax_progress.set_ylabel('Normalized Score', labelpad=10, fontsize=8)
            
            # Set x-axis ticks at sample positions
            self.ax_progress.set_xticks(range(n_samples))
            self.ax_progress.set_xticklabels([str(i+1) for i in range(n_samples)])
            
            # Set axis limits to ensure proper spacing
            self.ax_progress.set_xlim(-0.5, n_samples - 0.5)
            self.ax_progress.set_ylim(0, 1.0)
            
            # Grid styling
            self.ax_progress.grid(True, linestyle='--', alpha=0.7, axis='y')
            self.ax_progress.set_axisbelow(True)
            
            # Legend styling
            self.ax_progress.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
            
            # Adjust layout
            self.fig_progress.tight_layout(rect=[0, 0, 0.85, 1])
            self.canvas_progress.draw()
        
    def plot_final_radar(self, final_metrics):
        # Hide metric progress plot and show final frame
        self.plot_frame.grid_remove()
        self.final_frame.grid()
        
        # Clear radar plot
        self.ax_radar.clear()
        
        metrics = ['ROUGE-1', 'ROUGE-2', 'ROUGE-L', 'BLEU', 'METEOR', 'BERT-F1']
        raw_values = [
            final_metrics['rouge1'],
            final_metrics['rouge2'],
            final_metrics['rougeL'],
            final_metrics['bleu'],
            final_metrics['meteor'],
            final_metrics['bert_f1']
        ]
        normalized_values = [
            self.normalize_score('rouge1', final_metrics['rouge1']),
            self.normalize_score('rouge2', final_metrics['rouge2']),
            self.normalize_score('rougeL', final_metrics['rougeL']),
            self.normalize_score('bleu', final_metrics['bleu']),
            self.normalize_score('meteor', final_metrics['meteor']),
            self.normalize_score('bert_f1', final_metrics['bert_f1'])
        ]
        
        # Radar chart
        angles = np.linspace(0, 2*np.pi, 6, endpoint=False)
        values_closed = np.concatenate((normalized_values, [normalized_values[0]]))
        angles_closed = np.concatenate((angles, [angles[0]]))
        
        # Draw grid lines
        for i in [0.2, 0.4, 0.6, 0.8, 1.0]:
            self.ax_radar.plot(angles_closed, [i]*len(angles_closed), '--', color='gray', alpha=0.3)
        
        # Draw metric lines
        for angle in angles:
            self.ax_radar.plot([angle, angle], [0, 1], '--', color='gray', alpha=0.3)
        
        # Plot normalized data
        self.ax_radar.plot(angles_closed, values_closed, 'o-', linewidth=2, color='#4E79A7')
        self.ax_radar.fill(angles_closed, values_closed, alpha=0.25, color='#4E79A7')
        
        # Add raw score annotations with offset
        for angle, raw, norm in zip(angles, raw_values, normalized_values):
            # Calculate text position with offset
            text_radius = norm + 0.15  # Increase offset
            self.ax_radar.text(angle, text_radius, f'{raw:.3f}', 
                             ha='center', va='center', fontsize=6,
                             bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
        
        # Customize display
        self.ax_radar.set_xticks(angles)
        self.ax_radar.set_xticklabels(metrics, fontsize=6)
        self.ax_radar.set_ylim(0, 1.2)  # Increased to accommodate labels
        self.ax_radar.set_rgrids([0.2, 0.4, 0.6, 0.8, 1.0], angle=0, fontsize=6)
        self.ax_radar.set_title('Normalized Metrics Comparison', pad=15, fontsize=8, fontweight='bold')
        
        self.fig_radar.tight_layout()
        self.canvas_radar.draw()
        
    def clear_plots(self):
        # Function to reset plots for every update
        self.metrics_history = {k: [] for k in self.metrics_history}
        self.ax_progress.clear()
        self.ax_radar.clear()
        self.hide_plots()
        self.canvas_progress.draw()
        self.canvas_radar.draw()