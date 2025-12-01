import gradio as gr
import random
import matplotlib.pyplot as plt
import copy


# CLASS 1: The Core Function.

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
        # Clear any existing data
        self.data = []
        self.history = []
        
        # Loop 30 times to create 30 random numbers
        for i in range(count):
            # Pick a random number between 5 and 100
            random_num = random.randint(5, 100)
            self.data.append(random_num)
        
        # Save the initial state of the list to history
        # We use deepcopy to make sure we store the actual values, not just a reference
        self.history.append(copy.deepcopy(self.data))
        
        return self.data

    def merge_sort_entry(self):
        """
        Starts the merge sort process.
        """
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
            # We do this after every change so the visualization can shows properly.
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



# CLASS 2: The Visualization.

class VisualManager:
    """
    It converts the data list into a Matplotlib bar chart.
    """
    def create_chart(self, data_list, title="Merge Sort Visualization"):
        """
        Creates a bar chart figure based on the provided data.
        """
        # Create the figure and axis
        fig, ax = plt.subplots(figsize=(10, 6))
        
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
        plt.tight_layout()
        
        return fig



# MAIN APP SETUP


# Create instances of our logic and visual classes
sorter = MergeSortEngine()
visualizer = VisualManager()

def initialize_app():
    """
    Runs when the app starts or resets.
    Generates random data and returns the initial plot.
    """
    initial_data = sorter.generate_data()
    return visualizer.create_chart(initial_data, "Initial Random Data")

def run_simulation():
    """
    Runs the sort and yields plots.
    """
    # Get the history of all sorting steps
    history = sorter.merge_sort_entry()
    
    # Loop through each step in the history
    total_steps = len(history)
    for index, snapshot in enumerate(history):
        # Update the title with the current step number
        title_text = f"Sorting... Step {index + 1} of {total_steps}"
        
        # Create the chart for this step
        fig = visualizer.create_chart(snapshot, title_text)
        
        # Yield the figure to update the UI
        yield fig

# Define the Gradio layout
with gr.Blocks() as app:
    
    gr.Markdown("# 📉 Merge Sort Visualizer")
    gr.Markdown("Click **Start Sorting** to watch the Merge Sort algorithm.")
    
    with gr.Row():
        start_btn = gr.Button("Start Sorting", variant="primary")
        reset_btn = gr.Button("Generate New Data")
    
    # The output area for the chart
    plot_output = gr.Plot(label="Sorting Visualization")
    
    # Set up the event listeners
    # Load initial data on startup
    app.load(fn=initialize_app, inputs=None, outputs=plot_output)
    
    # Generate new data when Reset is clicked
    reset_btn.click(fn=initialize_app, inputs=None, outputs=plot_output)
    
    # Run the simulation when Start is clicked
    start_btn.click(fn=run_simulation, inputs=None, outputs=plot_output)

# Start the server
if __name__ == "__main__":
    app.launch()