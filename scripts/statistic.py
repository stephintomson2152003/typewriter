import json
import matplotlib.pyplot as plt
import numpy as np
import datetime
import os

# Load input history data from the local storage file (JSON format)
def load_input_history(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            if not isinstance(data, list):
                raise ValueError("Input history must be a list of sessions.")
            if len(data) == 0:
                raise ValueError("Input history is empty.")
            return data
    except FileNotFoundError:
        raise ValueError(f"The file '{filename}' does not exist. Please make sure it is available in the correct directory.")
    except json.JSONDecodeError:
        raise ValueError(f"The file '{filename}' is not a valid JSON. Please correct its format.")

# Calculate input speed (keys per minute) based on input history
def calculate_input_speed(session):
    input_history = session['history']
    if not input_history:
        return 0
    start_time = datetime.datetime.fromisoformat(input_history[0].get('timestamp'))
    end_time = datetime.datetime.fromisoformat(input_history[-1].get('timestamp'))
    duration_minutes = (end_time - start_time).total_seconds() / 60
    return len(input_history) / duration_minutes if duration_minutes > 0 else 0

# Calculate accuracy based on correct and incorrect keystrokes
def calculate_accuracy(session):
    input_history = session['history']
    total_keystrokes = len(input_history)
    correct_keystrokes = sum(1 for entry in input_history if entry.get('is_correct'))
    return (correct_keystrokes / total_keystrokes) * 100 if total_keystrokes > 0 else 0

# Calculate words per minute (WPM)
def calculate_words_per_minute(session):
    input_history = session['history']
    if not input_history:
        return 0
    start_time = datetime.datetime.fromisoformat(input_history[0].get('timestamp'))
    end_time = datetime.datetime.fromisoformat(input_history[-1].get('timestamp'))
    duration_minutes = (end_time - start_time).total_seconds() / 60
    correct_word_count = sum(1 for entry in input_history if entry.get('is_correct')) // 5  # Assuming 1 word = 5 correct characters
    return correct_word_count / duration_minutes if duration_minutes > 0 else 0

# Calculate raw statistics (correct, incorrect, backspaces used)
def calculate_raw_statistics(session):
    input_history = session['history']
    correct = sum(1 for entry in input_history if entry.get('is_correct'))
    incorrect = sum(1 for entry in input_history if not entry.get('is_correct'))
    backspaces = sum(1 for entry in input_history if entry.get('is_backspace'))
    return {"correct": correct, "incorrect": incorrect, "backspaces": backspaces}

# Function to sanitize the timestamp to make it valid for filenames
def sanitize_timestamp(timestamp):
    # Replace colons and other invalid characters with underscores
    return timestamp.replace(':', '_').replace('Z', '').replace('T', '_')

# Plot statistics and save them as images
def plot_statistics(input_history_data):
    if not input_history_data:
        print("No input history available to plot statistics.")
        return

    for session in input_history_data:
        score = session['score']
        level = session['level']
        input_history = session['history']

        input_speed = calculate_input_speed(session)
        accuracy = calculate_accuracy(session)
        words_per_minute = calculate_words_per_minute(session)
        raw_stats = calculate_raw_statistics(session)

        # Create time points for plotting
        time_points = list(range(1, len(input_history) + 1))
        wpm_values = [words_per_minute] * len(input_history)  # Simulating consistency in WPM
        error_values = [raw_stats["incorrect"]] * len(input_history)  # Fixed error count for simplicity

        fig, ax1 = plt.subplots(figsize=(12, 6))

        ax1.set_xlabel('Time Points')
        ax1.set_ylabel('Words per Minute', color='yellow')
        ax1.plot(time_points, wpm_values, color='yellow', label='WPM', linewidth=2)
        ax1.tick_params(axis='y', labelcolor='yellow')

        ax2 = ax1.twinx()
        ax2.set_ylabel('Errors', color='red')
        ax2.plot(time_points, error_values, 'r-', label='Errors', marker='x')
        ax2.tick_params(axis='y', labelcolor='red')

        fig.tight_layout()

        # Create output directory if it doesn't exist
        output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Sanitize the timestamp for valid filename
        sanitized_timestamp = sanitize_timestamp(session["timestamp"])

        # Save the plot as an image
        output_path = os.path.join(output_dir, f'statistics_{sanitized_timestamp}.png')
        plt.savefig(output_path)
        plt.close()

        print(f"Statistics graph saved at {output_path}")

        # Save statistics data
        stats = {
            "input_speed": input_speed,
            "accuracy": accuracy,
            "words_per_minute": words_per_minute,
            "raw_statistics": raw_stats,
            "score": score,
            "level": level
        }
        stats_path = os.path.join(output_dir, f'statistics_{sanitized_timestamp}.json')
        with open(stats_path, 'w') as stats_file:
            json.dump(stats, stats_file, indent=2)
        print(f"Statistics data saved at {stats_path}")

if __name__ == "__main__":
    print("Starting statistic script...")
    try:
        input_history_data = load_input_history('../input_history.json')
        print("Loaded input history successfully")
        plot_statistics(input_history_data)
        print("Plotted statistics successfully")
    except ValueError as e:
        print(f"Error: {e}")
