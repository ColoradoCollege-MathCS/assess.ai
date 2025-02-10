

from pathlib import Path
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.widgets import Slider
import numpy as np

# Reference to slider code: https://stackoverflow.com/questions/44791466/scrollable-bar-graph-matplotlib
class EvaluationVisualizer:
    def __init__(self, root):
        self.root = root
        self.metrics_history = {
            'rouge1': [],
            'rouge2': [],
            'rougeL': [],
            'bleu': [],
            'meteor': [],
            'bert_f1': [],
            'coherence': [],
            'consistency': [],
            'fluency': [],
            'relevance': []
        }
        # Separate dictionary for G-EVAL metrics to avoid normalization
        self.geval_metrics = ['coherence', 'consistency', 'fluency', 'relevance']
        # Define typical ranges for each metric
        self.metric_ranges = {
            'rouge1': (0.0, 0.5),
            'rouge2': (0.0, 0.45),
            'rougeL': (0.0, 0.48),
            'bleu': (0.0, 0.5),
            'meteor': (0.0, 0.35),
            'bert_f1': (0.0, 0.8)
        }
        self.visible_samples = 4  # Show 4 samples at a time
        self.current_traditional_pos = 0
        self.current_geval_pos = 0
        self.setup_plots()
        
    def normalize_score(self, metric, value):
        # min-max normalization formula. Used here since outliers aren't an issue and we can guarantee fixed range from 0-1
        min_val, max_val = self.metric_ranges[metric]
        normalized = (value - min_val) / (max_val - min_val)
        return max(0, min(1, normalized))
    
    def setup_plots(self):
        # Create frames for plots
        self.plot_frame_traditional = tk.Frame(self.root, bg="white")
        self.plot_frame_traditional.grid(row=6, column=0, columnspan=3, sticky="nsew", padx=20, pady=(0, 5))
        
        self.plot_frame_geval = tk.Frame(self.root, bg="white")
        self.plot_frame_geval.grid(row=7, column=0, columnspan=3, sticky="nsew", padx=20, pady=5)
        
        # Hide initially
        self.plot_frame_traditional.grid_remove()
        self.plot_frame_geval.grid_remove()
        
        # Progress plots
        self.fig_traditional = Figure(figsize=(12, 3))
        self.ax_traditional = self.fig_traditional.add_axes([0.1, 0.2, 0.75, 0.7])
        self.fig_traditional.patch.set_facecolor('#FFFFFF')
        self.ax_traditional.set_facecolor('#F8F9FA')

        # Add slider axes for traditional metrics
        self.slider_ax_traditional = self.fig_traditional.add_axes([0.1, 0.05, 0.75, 0.03])
        self.slider_traditional = Slider(
            self.slider_ax_traditional, 'Position', 0, 1,
            valinit=0, valstep=1, color='skyblue',
            initcolor=None # Important for slider interactivity
        )
        # Hides labels for slider
        self.slider_traditional.valtext.set_visible(False)
        
        # Connect the slider to tkinter event handling
        self.slider_traditional.on_changed(self._on_traditional_slider_change)
        self.canvas_traditional = FigureCanvasTkAgg(self.fig_traditional, master=self.plot_frame_traditional)
        self.canvas_traditional_widget = self.canvas_traditional.get_tk_widget()
        self.canvas_traditional_widget.pack(fill=tk.BOTH, expand=True)
        
        # Setup G-EVAL plot
        self.fig_geval = Figure(figsize=(10, 3.5))
        self.ax_geval = self.fig_geval.add_axes([0.1, 0.2, 0.75, 0.7])
        self.fig_geval.patch.set_facecolor('#FFFFFF')
        self.ax_geval.set_facecolor('#F8F9FA')

        # Add slider axes for G-EVAL metrics
        self.slider_ax_geval = self.fig_geval.add_axes([0.1, 0.05, 0.75, 0.03])
        self.slider_geval = Slider(
            self.slider_ax_geval, 'Position', 0, 1,
            valinit=0, valstep=1, color='skyblue',
            initcolor=None # Important for slider interactivity
        )
        self.slider_geval.valtext.set_visible(False)
        
        # Connect the slider to tkinter event handling
        self.slider_geval.on_changed(self._on_geval_slider_change)
        self.canvas_geval = FigureCanvasTkAgg(self.fig_geval, master=self.plot_frame_geval)
        self.canvas_geval_widget = self.canvas_geval.get_tk_widget()
        self.canvas_geval_widget.pack(fill=tk.BOTH, expand=True)
        
        # Initialize radar charts
        self.final_frame = tk.Frame(self.root, bg="white")
        self.final_frame.grid(row=8, column=0, columnspan=3, sticky="nsew", padx=20, pady=10)
        self.final_frame.grid_remove()
        self.fig_radar = Figure(figsize=(8, 3))
        self.ax_radar_traditional = self.fig_radar.add_subplot(121, projection='polar')
        self.ax_radar_geval = self.fig_radar.add_subplot(122, projection='polar')
        self.canvas_radar = FigureCanvasTkAgg(self.fig_radar, master=self.final_frame)
        self.canvas_radar_widget = self.canvas_radar.get_tk_widget()
        self.canvas_radar_widget.pack(fill=tk.BOTH, expand=True)

    def show_plots(self, use_geval=True):
            self.plot_frame_traditional.grid()
            if use_geval:
                self.plot_frame_geval.grid()
        
    def hide_plots(self):
        self.plot_frame_traditional.grid_remove()
        self.plot_frame_geval.grid_remove()
        self.final_frame.grid_remove()
    
    def clear_plots(self):
        # Reset all metric histories to empty lists while keeping the same keys
        self.metrics_history = {k: [] for k in self.metrics_history}
        
        # Clear plots
        self.ax_traditional.clear()
        self.ax_geval.clear()
        self.ax_radar_traditional.clear()
        self.ax_radar_geval.clear()
        
        # Reset slider positions
        self.current_traditional_pos = 0
        self.current_geval_pos = 0
        self.slider_traditional.set_val(0)
        self.slider_geval.set_val(0)
        
        # Remove all plot frames from the grid layout
        self.hide_plots()
        # Refresh the traditional metrics canvas to show empty plot
        self.canvas_traditional.draw()
        
        # Refresh the G-EVAL metrics canvas to show empty plot
        self.canvas_geval.draw()
        
        # Refresh the radar plot canvas to show empty plot
        self.canvas_radar.draw()
        
    def _on_traditional_slider_change(self, val):
        self.current_traditional_pos = int(val)
        # Update the visuals of the traditional plot after 10ms. 
        self.root.after(10, self._update_traditional_plot)
        
    def _on_geval_slider_change(self, val):
        # Same for GEVAL
        self.current_geval_pos = int(val)
        self.root.after(10, self._update_geval_plot)
        
    def _update_traditional_plot(self):
        # Gets all metric values from the dictionary,  Gets the first sequence of values from the iterator, 
        # Gets the length of this sequence, Checks if there's at least one data point to plot (length > 0). 
        # If so plot all bar charts with the starting sample being the scroller's position. Sets Normalization as True 
        if len(next(iter(self.metrics_history.values()))) > 0:
            self._plot_metrics(self.ax_traditional, 
                             ['rouge1', 'rouge2', 'rougeL', 'bleu', 'meteor', 'bert_f1'],
                             ['#4E79A7', '#F28E2B', '#E15759', '#76B7B2', '#59A14F', '#EDC948'],
                             self.current_traditional_pos, True)
            self.canvas_traditional.draw()
            
    def _update_geval_plot(self):
        # _update_traditional_plot for GEVAL
        if len(next(iter(self.metrics_history.values()))) > 0:
            self._plot_metrics(self.ax_geval,
                             ['coherence', 'consistency', 'fluency', 'relevance'],
                             ['#AF7AA1', '#FF9DA7', '#9C755F', '#BAB0AC'],
                             self.current_geval_pos, False)
            self.canvas_geval.draw()

    def _plot_metrics(self, ax, metrics, colors, start_pos, normalize=True):
        ax.clear()
        n_metrics = len(metrics)
        bar_width = 0.15 
        n_samples = len(next(iter(self.metrics_history.values())))
        
        # Calculate visible range
        # # If: start_pos = 2 self.visible_samples = 4 n_samples = 5
        # Then: start_pos + self.visible_samples = 6 min(6, 5) = 5  
        # # Prevents going beyond data length
        end_pos = min(start_pos + self.visible_samples, n_samples)
        visible_range = range(start_pos, end_pos)
        
        for idx, (metric, color) in enumerate(zip(metrics, colors)):
            # Position bars with fixed spacing
            positions = np.arange(len(visible_range)) + (idx - n_metrics/2) * bar_width
            raw_values = [self.metrics_history[metric][i] if self.metrics_history[metric][i] is not None else 0.0 
                         for i in visible_range]
            
            if normalize and metric not in self.geval_metrics:
                values = [self.normalize_score(metric, v) for v in raw_values]
                label = f'{metric}'
            else:
                values = raw_values
                label = metric
                
            ax.bar(positions, values, bar_width,
                  label=label, color=color, alpha=0.8,
                  edgecolor='black', linewidth=1)
        
        ax.set_xlabel('Samples Processed', labelpad=20, fontsize=8,)
        ax.set_ylabel('Score', labelpad=10, fontsize=8)
        ax.set_xticks(range(len(visible_range)))
        ax.set_xticklabels([str(i+1) for i in visible_range])
        
        # Set fixed x-axis limits to maintain consistent bar sizes
        ax.set_xlim(-0.5, len(visible_range) - 0.5)
        
        ax.grid(True, linestyle='--', alpha=0.7, axis='y')
        ax.set_axisbelow(True)
        ax.legend(bbox_to_anchor=(1.0, 1), loc='upper left', fontsize=8)
        
        if normalize:
            ax.set_ylim(0, 1.1)
            ax.set_title('Traditional Metrics Progress (Normalized)', pad=5, fontsize=10, fontweight='bold')
        else:
            ax.set_ylim(0, 5.5)
            ax.set_title('G-EVAL Metrics Progress', pad=5, fontsize=10, fontweight='bold')
        
    def update_plots(self, metrics, use_geval=True):
        # Update metrics for every new sample
        for metric, value in metrics.items():
            if metric in self.metrics_history:
                self.metrics_history[metric].append(value)
        
        # Only show and update plot if we have at least 1 sample
        n_samples = len(next(iter(self.metrics_history.values())))
        self.show_plots(use_geval)
        
        # Update slider ranges, get the 
        max_slider_val = max(0, n_samples - self.visible_samples)
        # Reset slider range and value
        self.slider_traditional.valmin = 0
        self.slider_traditional.valmax = max_slider_val
        self.slider_traditional.valinit = max_slider_val  # Set slider to maximum value
        self.slider_traditional.ax.set_xlim(0, max_slider_val)
        
        if use_geval:
            self.slider_geval.valmin = 0
            self.slider_geval.valmax = max_slider_val
            self.slider_geval.valinit = max_slider_val  # Set slider to maximum value
            self.slider_geval.ax.set_xlim(0, max_slider_val)
        
        # Set sliders to end position
        self.current_traditional_pos = max_slider_val
        self.current_geval_pos = max_slider_val
        self.slider_traditional.set_val(max_slider_val)
        if use_geval:
            self.slider_geval.set_val(max_slider_val)
        
        # Initial plot updates
        self._update_traditional_plot()
        if use_geval:
            self._update_geval_plot()
        
        # Redraw sliders
        self.slider_traditional.ax.figure.canvas.draw()
        if use_geval:
            self.slider_geval.ax.figure.canvas.draw()

    def plot_final_radar(self, final_metrics, use_geval=True):
        # Hide both progress plots
        self.plot_frame_traditional.grid_remove()
        self.plot_frame_geval.grid_remove()
        self.final_frame.grid()
        
        # Traditional metrics
        traditional_metrics = ['ROUGE-1', 'ROUGE-2', 'ROUGE-L', 'BLEU', 'METEOR', 'BERT-F1']
        traditional_values = [
            final_metrics['rouge1'],
            final_metrics['rouge2'],
            final_metrics['rougeL'],
            final_metrics['bleu'],
            final_metrics['meteor'],
            final_metrics['bert_f1']
        ]
        traditional_normalized = [
            self.normalize_score('rouge1', final_metrics['rouge1']),
            self.normalize_score('rouge2', final_metrics['rouge2']),
            self.normalize_score('rougeL', final_metrics['rougeL']),
            self.normalize_score('bleu', final_metrics['bleu']),
            self.normalize_score('meteor', final_metrics['meteor']),
            self.normalize_score('bert_f1', final_metrics['bert_f1'])
        ]
        
        # Create evenly spaced angles from 0 to 2π (not including 2π) for each metric
        angles_trad = np.linspace(0, 2*np.pi, len(traditional_metrics), endpoint=False)

        # Create a closed shape by adding the first value to the end of normalized values
        # This connects the last point back to the first point in the radar plot
        values_closed_trad = np.concatenate((traditional_normalized, [traditional_normalized[0]]))

        # Similarly, create closed angles by adding the first angle to the end
        # This ensures the plot lines form a complete polygon
        angles_closed_trad = np.concatenate((angles_trad, [angles_trad[0]]))

        # Create circular grid lines at different radius values (0.2, 0.4, etc.)
        for i in [0.2, 0.4, 0.6, 0.8, 1.0]:
            self.ax_radar_traditional.plot(angles_closed_trad, [i]*len(angles_closed_trad), 
                                        '--', color='gray', alpha=0.3)
        
        # Create radial grid lines from center to edge
        for angle in angles_trad:
            self.ax_radar_traditional.plot([angle, angle], [0, 1], 
                                        '--', color='gray', alpha=0.3)

        # Fill the area inside the radar plot with a semi-transparent color. alpha=0.25 makes the fill 75% transparent
        self.ax_radar_traditional.plot(angles_closed_trad, values_closed_trad, 
                                    'o-', linewidth=2, color='#4E79A7')
        self.ax_radar_traditional.fill(angles_closed_trad, values_closed_trad, 
                                    alpha=0.25, color='#4E79A7')
        
        # Add raw score annotations for traditional metrics
        for angle, raw, norm in zip(angles_trad, traditional_values, traditional_normalized):
            text_radius = norm + 0.15
            self.ax_radar_traditional.text(angle, text_radius, f'{raw:.3f}',
                                        ha='center', va='center', fontsize=6,
                                        bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
            
        # Plot G-EVAL metrics radar if enabled
        if use_geval:
            geval_metrics = ['Coherence', 'Consistency', 'Fluency', 'Relevance']
            geval_values = [
                final_metrics['coherence'],
                final_metrics['consistency'],
                final_metrics['fluency'],
                final_metrics['relevance']
            ]
            
            # Divides circle into angles for radar chart
            angles_geval = np.linspace(0, 2*np.pi, len(geval_metrics), endpoint=False)
            # Add the first value to the end of the values list. Makes the polygon close by connecting back to start
            values_closed_geval = np.concatenate((geval_values, [geval_values[0]]))
            angles_closed_geval = np.concatenate((angles_geval, [angles_geval[0]]))
            
            # Draw circular grid lines at score values 1-5 
            for i in [1, 2, 3, 4, 5]:
                self.ax_radar_geval.plot(angles_closed_geval, [i]*len(angles_closed_geval), '--', color='gray', alpha=0.3)
            
            # Draw radial lines from center (0) to edge (5) for each metric
            for angle in angles_geval:
                self.ax_radar_geval.plot([angle, angle], [0, 5], '--', color='gray', alpha=0.3)
                
            self.ax_radar_geval.plot(angles_closed_geval, values_closed_geval, 'o-', linewidth=2, color='#AF7AA1')
            self.ax_radar_geval.fill(angles_closed_geval, values_closed_geval, alpha=0.25, color='#AF7AA1')
            
            # Add score annotations for G-EVAL metrics
            for angle, value in zip(angles_geval, geval_values):
                text_radius = value + 0.5
                self.ax_radar_geval.text(angle, text_radius, f'{value:.3f}',
                                       ha='center', va='center', fontsize=6,
                                       bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
        
        # Customize traditional radar display
        self.ax_radar_traditional.set_xticks(angles_trad)
        self.ax_radar_traditional.set_xticklabels(traditional_metrics, fontsize=6)
        self.ax_radar_traditional.set_ylim(0, 1.2)
        self.ax_radar_traditional.set_rgrids([0.2, 0.4, 0.6, 0.8, 1.0], angle=0, fontsize=6)
        title = 'Traditional Metrics (Normalized)'
        if not use_geval:
            title = 'Evaluation Metrics (Normalized)'
        self.ax_radar_traditional.set_title(title, pad=15, fontsize=8, fontweight='bold')
        
        # Customize G-EVAL radar display
        if use_geval:
            self.ax_radar_geval.set_xticks(angles_geval)
            self.ax_radar_geval.set_xticklabels(geval_metrics, fontsize=6)
            self.ax_radar_geval.set_ylim(0, 5.5)
            self.ax_radar_geval.set_rgrids([1, 2, 3, 4, 5], angle=0, fontsize=6)
            self.ax_radar_geval.set_title('G-EVAL Metrics\n(Raw Scores)', pad=15, fontsize=8, fontweight='bold')
        
        # Adjust layout based on G-EVAL toggle
        if use_geval:
            self.fig_radar.tight_layout(pad=2.0)
            self.ax_radar_traditional.set_visible(True)
            self.ax_radar_geval.set_visible(True)
        else:
            # If G-EVAL is disabled, only show traditional metrics and center it
            self.ax_radar_traditional.set_position([0.1, 0.1, 0.8, 0.8])
            self.ax_radar_geval.set_visible(False)
            
        self.canvas_radar.draw()

    def save_plots(self, save_dir):
        try:
            # Ensure directory exists
            save_dir = Path(save_dir)
            save_dir.mkdir(parents=True, exist_ok=True)
            
            # Store original settings
            original_visible_samples = self.visible_samples
            original_traditional_pos = self.current_traditional_pos
            original_geval_pos = self.current_geval_pos
            
            # Create new figure for full traditional metrics
            full_fig_traditional = Figure(figsize=(16, 4))  # Larger figure for all samples
            full_ax_traditional = full_fig_traditional.add_axes([0.1, 0.15, 0.85, 0.75])  # Adjusted axes for better visibility
            
            # Get total number of samples
            n_samples = len(next(iter(self.metrics_history.values())))
            
            # Temporarily set visible_samples to show all data
            self.visible_samples = n_samples
            
            # Plot all traditional metrics
            self._plot_metrics(
                full_ax_traditional,
                ['rouge1', 'rouge2', 'rougeL', 'bleu', 'meteor', 'bert_f1'],
                ['#4E79A7', '#F28E2B', '#E15759', '#76B7B2', '#59A14F', '#EDC948'],
                0,  # Start from beginning
                True  # Normalize
            )
            
            # Save full traditional metrics plot
            full_fig_traditional.savefig(
                save_dir / 'traditional_metrics_full.png',
                bbox_inches='tight',
                dpi=300,
                facecolor='white'
            )
            
            # If G-EVAL metrics are enabled, save them too
            if self.plot_frame_geval.winfo_ismapped():
                full_fig_geval = Figure(figsize=(16, 4))
                full_ax_geval = full_fig_geval.add_axes([0.1, 0.15, 0.85, 0.75])
                
                self._plot_metrics(
                    full_ax_geval,
                    ['coherence', 'consistency', 'fluency', 'relevance'],
                    ['#AF7AA1', '#FF9DA7', '#9C755F', '#BAB0AC'],
                    0,  # Start from beginning
                    False  # Don't normalize G-EVAL metrics
                )
                
                full_fig_geval.savefig(
                    save_dir / 'geval_metrics_full.png',
                    bbox_inches='tight',
                    dpi=300,
                    facecolor='white'
                )
            
            # Save radar plot if visible
            if self.final_frame.winfo_ismapped():
                self.fig_radar.savefig(
                    save_dir / 'final_radar_plot.png',
                    bbox_inches='tight',
                    dpi=300,
                    facecolor='white'
                )
            
            # Restore original settings
            self.visible_samples = original_visible_samples
            self.current_traditional_pos = original_traditional_pos
            self.current_geval_pos = original_geval_pos
            
            # Update the plots to restore original view
            self._update_traditional_plot()
            if self.plot_frame_geval.winfo_ismapped():
                self._update_geval_plot()
                
        except Exception as e:
            print(f"Error saving plots: {str(e)}")