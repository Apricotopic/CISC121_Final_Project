import gradio as gr
import random
import copy
# We import Figure directly to avoid memory leaks caused by pyplot's global state
from matplotlib.figure import Figure


# CLASS 1: The Core Function (Model)

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
        
        # Save the initial state of the list to history
        self.history.append(copy.deepcopy(self.data))
        
        return self.data

    def merge_sort_entry(self):
        """
        Starts the merge sort process.
        """
        # Clear history before starting a new sort to prevent memory buildup
        # We keep the current state as the starting point
        self.history = [copy.deepcopy(self.data)]
        
        # Call the recursive sorting function on the whole list
        self.merge_sort_recursive(self.data, 0, len(self.data) - 1)
        
        # Return the complete history so the UI can show the animation
        return self.history

    def merge_sort_recursive(self, arr, left_index, right_index):
        """
        Recursively splits the list into smaller halves.
        """
        # If the list has only 1 item or is empty, stop splitting
        if left_index >= right_index:
            return

        # Calculate the middle index
        mid_index = (left_index + right_index) // 2

        # Sort the left half
        self.merge_sort_recursive(arr, left_index, mid_index)
        
        # Sort the right half
        self.merge_sort_recursive(arr, mid_index + 1, right_index)

        # Merge the two sorted halves back together
        self.merge(arr, left_index, mid_index, right_index)

    def merge(self, arr, left, mid, right):
        """
        Merges two sorted sub-lists back into the main list.
        """
        # Create temporary copies of the left and right parts
        left_half = arr[left : mid + 1]
        right_half = arr[mid + 1 : right + 1]

        i = 0 # Index for left_half
        j = 0 # Index for right_half
        k = left # Index for the main array

        # Compare items from both halves and put the smaller one into the main array
        while i < len(left_half) and j < len(right_half):
            if left_half[i] <= right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1
            
            # Save the current state of the list to history
            # We do this after every change so the visualization updates properly
            self.history.append(copy.deepcopy(self.data))

        # If there are items left in the left_half, add them to the main array
        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1
            # Save state
            self.history.append(copy.deepcopy(self.data))

        # If there are items left in the right_half, add them to the main array
        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1
            # Save state
            self.history.append(copy.deepcopy(self.data))



# CLASS 2: The Visualization (View)

class VisualManager:
    """
    It converts the data list into a Matplotlib bar chart.
    """
    def create_chart(self, data_list, title="Merge Sort Visualization"):
        """
        Creates a bar chart figure based on the provided data.
        """

        fig = Figure(figsize=(10, 6))
        ax = fig.subplots()
        
        # Generate indices for the x-axis (0, 1, 2, ...)
        indices = range(len(data_list))
        
        # Draw the bars
        # I chose a specific color hex code for better aesthetics
        ax.bar(indices, data_list, color='#4F46E5')
        
        # Set the labels and title
        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.set_xlabel('Index', fontsize=12)
        ax.set_ylabel('Value', fontsize=12)
        
        # Set a fixed height for the y-axis so the chart doesn't rescale constantly
        ax.set_ylim(0, 110)
        
        # Adjust layout to prevent clipping
        fig.tight_layout()
        
        return fig



# MAIN APP SETUP

visualizer = VisualManager()

def initialize_app():
    """
    Runs when the app starts or resets.
    Creates a new sorter instance for this specific user session.
    Returns the new sorter object and the initial plot.
    """
    # Create a fresh engine for this user
    new_sorter = MergeSortEngine()
    initial_data = new_sorter.generate_data()
    
    # Create the chart
    fig = visualizer.create_chart(initial_data, "Initial Random Data")
    
    # Return the chart AND the sorter instance (to be stored in State)
    return fig, new_sorter

def run_simulation(current_sorter):
    """
    Runs the sort using the user's specific sorter instance.
    """
    # If no sorter exists (e.g. page just loaded), create one
    if current_sorter is None:
        current_sorter = MergeSortEngine()
        current_sorter.generate_data()

    # Get the history of all sorting steps
    history = current_sorter.merge_sort_entry()
    
    # Loop through each step in the history
    total_steps = len(history)
    for index, snapshot in enumerate(history):
        # Update the title with the current step number
        title_text = f"Sorting... Step {index + 1} of {total_steps}"
        
        # Create the chart for this step
        fig = visualizer.create_chart(snapshot, title_text)
        
        # Yield the figure to update the UI
        yield fig


# Define the layout
with gr.Blocks() as app:
    
    gr.Markdown("# 📉 Merge Sort Visualizer")
    gr.Markdown("Click **Start Sorting** to watch the Merge Sort algorithm.")
    
    with gr.Row():
        start_btn = gr.Button("Start Sorting", variant="primary")
        reset_btn = gr.Button("Generate New Data")
    
    # The output area for the chart
    plot_output = gr.Plot(label="Sorting Visualization")
    
    # This prevents users from interfering with each other's sorting data.
    sorter_state = gr.State()

    
    # 1. On Page Load: Initialize data and store the sorter in 'sorter_state'
    app.load(fn=initialize_app, inputs=None, outputs=[plot_output, sorter_state])
    
    # 2. On Reset: Create new data/sorter and update 'sorter_state'
    reset_btn.click(fn=initialize_app, inputs=None, outputs=[plot_output, sorter_state])
    
    # 3. On Start: Use the sorter from 'sorter_state' to run the simulation
    start_btn.click(fn=run_simulation, inputs=[sorter_state], outputs=plot_output)

# Start the server
if __name__ == "__main__":
    app.launch()