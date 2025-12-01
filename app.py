import gradio as gr
import random
import copy

from matplotlib.figure import Figure


# CLASS 1: The Core Function
class MergeSortEngine:
    """
    This class handles the data and the sorting algorithm.
    It stores the list of numbers and records the history of changes.
    """
    def __init__(self):
        # This list will hold the random numbers
        self.data = []
        # This list will store a copy of the data at every step
        self.history = []

    def generate_data(self, count=30):
        """
        Generates a new list of random integers.
        """
        # Clear any existing data to ensure a fresh start
        self.data = []
        self.history = []
        
        # Loop 30 times to create 30 random numbers
        for i in range(count):
            # Pick a random number between 5 and 100
            random_num = random.randint(5, 100)
            self.data.append(random_num)
        
        # Save the initial state. 
        # The second element [] means "no bars are active right now".
        self.history.append((copy.deepcopy(self.data), []))
        
        return self.data

    def merge_sort_entry(self):
        """
        Starts the merge sort process.
        """
        # Clear history and save starting state
        self.history = [(copy.deepcopy(self.data), [])]
        
        # Call the recursive sorting function on the whole list
        self.merge_sort_recursive(self.data, 0, len(self.data) - 1)
        
        # Return the complete history
        return self.history

    def merge_sort_recursive(self, arr, left_index, right_index):
        """
        Recursively splits the list into smaller halves.
        """
        if left_index >= right_index:
            return

        mid_index = (left_index + right_index) // 2

        self.merge_sort_recursive(arr, left_index, mid_index)
        self.merge_sort_recursive(arr, mid_index + 1, right_index)

        self.merge(arr, left_index, mid_index, right_index)

    def merge(self, arr, left, mid, right):
        """
        Merges two sorted sub-lists back into the main list.
        """
        left_half = arr[left : mid + 1]
        right_half = arr[mid + 1 : right + 1]

        i = 0 
        j = 0 
        k = left 

        while i < len(left_half) and j < len(right_half):
            if left_half[i] <= right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            
            # SNAPSHOT WITH HIGHLIGHT
            # This 'k' will be colored red in the visualizer.
            self.history.append((copy.deepcopy(self.data), [k]))
            
            k += 1

        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            
            # Snapshot with highlight on k
            self.history.append((copy.deepcopy(self.data), [k]))
            
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            
            # Snapshot with highlight on k
            self.history.append((copy.deepcopy(self.data), [k]))
            
            k += 1



# CLASS 2: The Visualization
class VisualManager:
    """
    It converts the data list into a Matplotlib bar chart.
    """
    def create_chart(self, snapshot, title="Merge Sort Visualization"):
        """
        Creates a bar chart figure.
        snapshot: A tuple containing (data_list, active_indices)
        """
        data_list, active_indices = snapshot
        
        fig = Figure(figsize=(10, 6))
        ax = fig.subplots()

        bar_colors = ['#4F46E5'] * len(data_list)
        
        # Highlight color is Red (#EF4444) for high contrast
        for index in active_indices:
            if index < len(bar_colors):
                bar_colors[index] = '#EF4444'
        
        # 2. Draw Bars
        indices = range(len(data_list))
        ax.bar(indices, data_list, color=bar_colors)
        
        # 3. Styling
        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.set_xlabel('Index', fontsize=12)
        ax.set_ylabel('Value', fontsize=12)
        ax.set_ylim(0, 110)
        
        fig.tight_layout()
        
        return fig



# MAIN APP SETUP
visualizer = VisualManager()

def initialize_app():
    """
    Runs on start/reset. 
    """
    new_sorter = MergeSortEngine()
    initial_data = new_sorter.generate_data()
    
    initial_snapshot = (initial_data, [])
    
    fig = visualizer.create_chart(initial_snapshot, "Initial Random Data")
    return fig, new_sorter

def run_simulation(current_sorter):
    """
    Runs the simulation loop.
    """
    if current_sorter is None:
        current_sorter = MergeSortEngine()
        current_sorter.generate_data()

    history = current_sorter.merge_sort_entry()
    
    total_steps = len(history)
    for index, snapshot in enumerate(history):
        title_text = f"Sorting... Step {index + 1} of {total_steps}"
        
        # Pass the full snapshot (data + highlights) to the visualizer
        fig = visualizer.create_chart(snapshot, title_text)
        
        yield fig

# Define the layout
with gr.Blocks() as app:
    
    gr.Markdown("# 📉 Merge Sort Visualizer")
    gr.Markdown("Click **Start Sorting** to watch the Merge Sort algorithm.")
    gr.Markdown("🟦 Static or Sorted parts | 🟥 Currently being adjusted")
    
    with gr.Row():
        start_btn = gr.Button("Start Sorting", variant="primary")
        reset_btn = gr.Button("Generate New Data")
    
    plot_output = gr.Plot(label="Sorting Visualization")
    
    sorter_state = gr.State()

    app.load(fn=initialize_app, inputs=None, outputs=[plot_output, sorter_state])
    reset_btn.click(fn=initialize_app, inputs=None, outputs=[plot_output, sorter_state])
    start_btn.click(fn=run_simulation, inputs=[sorter_state], outputs=plot_output)

if __name__ == "__main__":
    app.launch()