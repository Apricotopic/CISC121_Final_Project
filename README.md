---
title: CISC121 Final Project
emoji: 🐢
colorFrom: pink
colorTo: gray
sdk: gradio
sdk_version: 6.0.1
app_file: app.py
pinned: false
short_description: One of assignment for Queen's CISC121 course
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference



### **Problem Decomposition**

* Break the problem into sub-parts:  
  1. **Random Data Generation**: Implement a function to generate a randomized list of 30 integers to serve as the initial dataset.  
  2. **Recursive Divide**: Create a recursive function that continuously divides the list into halves until atomic sub-lists are reached.  
  3. **Conquer**: Implement the logic to merge two sorted sub-lists back into a single sorted list by comparing elements sequentially.  
  4. **Visualization**: Integrate a mechanism to record the state of the list after every data modification during the merge process to enable frame-by-frame animation.

### **Pattern Recognition**

* Similarities to known problems:  
  * **Divide and Conquer Strategy**
  * **Recursive Tree Traversal**
### **Abstraction**

* Ignore unnecessary details, focus on:  
  * **Inputs needed**: The list size (fixed at 30 for visualization) and value range. We ignore user-defined array sizes for simplicity in the UI.  
  * **Outputs required**: An ordered sequence of list states rather than just the final sorted list.  
  * **Core relationships**: The essential comparison logic: if Left\[i\] \<= Right\[j\], append Left\[i\] to the result; otherwise, append Right\[j\].

### **Algorithmic Thinking**

* **Inputs**: An unsorted list A containing N integers (where N=30).  
* **Outputs**: A series of lists \[A\_0, A\_1, ..., A\_k\] representing the state of the array at each step k of the sorting process, concluding with the fully sorted list.  
* **Constraints**:  
  * List size limited to 30 elements to ensure the bar chart remains readable in the GUI.  
  * Value range 5-100 to fit strictly within the y-axis chart limits.  
  * The visualization must reflect the O(N log N) complexity logic, showing the "grouping" effect of merge sort.