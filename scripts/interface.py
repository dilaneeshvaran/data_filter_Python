import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import json
from data_loader import load_csv, load_json, load_yaml, load_xml
from data_saver import save_csv, save_json, save_yaml, save_xml
from data_filter import filter_data, calculate_global_stats
from data_sorter import sort_data
from data_stat import calculate_statistics


class DataApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Management App")
        self.data = None

        self.create_widgets()

    def create_widgets(self):
        self.load_button = tk.Button(self.root, text="Load Data", command=self.load_data)
        self.load_button.pack()

        self.save_button = tk.Button(self.root, text="Save Data", command=self.save_data)
        self.save_button.pack()

        self.filter_button = tk.Button(self.root, text="Filter Data", command=self.filter_data)
        self.filter_button.pack()

        self.sort_button = tk.Button(self.root, text="Sort Data", command=self.sort_data)
        self.sort_button.pack()

        self.stats_button = tk.Button(self.root, text="Show Statistics", command=self.show_statistics)
        self.stats_button.pack()

        self.output_text = tk.Text(self.root, height=20, width=80)
        self.output_text.pack()

    def load_data(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            ext = file_path.split('.')[-1]
            if ext == 'csv':
                self.data = load_csv(file_path)
            elif ext == 'json':
                self.data = load_json(file_path)
            elif ext == 'yaml':
                self.data = load_yaml(file_path)
            elif ext == 'xml':
                self.data = load_xml(file_path)
            else:
                messagebox.showerror("Error", "Unsupported file format")
                return
            self.display_data(self.data)

    def save_data(self):
        if self.data is None:
            messagebox.showerror("Error", "No data to save")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                 filetypes=[("JSON files", "*.json"), ("CSV files", "*.csv"),
                                                            ("YAML files", "*.yaml"), ("XML files", "*.xml")])
        if file_path:
            ext = file_path.split('.')[-1]
            if ext == 'csv':
                save_csv(self.data, file_path)
            elif ext == 'json':
                save_json(self.data, file_path)
            elif ext == 'yaml':
                save_yaml(self.data, file_path)
            elif ext == 'xml':
                save_xml(self.data, file_path)
            else:
                messagebox.showerror("Error", "Unsupported file format")

    def filter_data(self):
        if self.data is None:
            messagebox.showerror("Error", "No data to filter")
            return
        criteria = simpledialog.askstring("Input", "Enter filter criteria (e.g., 'age>20'):")
        if criteria:
            global_stats = calculate_global_stats(self.data)
            criteria_list = self.parse_criteria(criteria)
            self.data = filter_data(self.data, criteria_list, global_stats)
            self.display_data(self.data)

    def sort_data(self):
        if self.data is None:
            messagebox.showerror("Error", "No data to sort")
            return
        sort_keys = simpledialog.askstring("Input", "Enter sort keys (e.g., 'lastname,firstname'):")
        if sort_keys:
            sort_keys_list = sort_keys.split(',')
            self.data = sort_data(self.data, sort_keys_list)
            self.display_data(self.data)

    def show_statistics(self):
        if self.data is None:
            messagebox.showerror("Error", "No data to show statistics")
            return
        stats = calculate_statistics(self.data)
        self.display_data(stats)

    def display_data(self, data):
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, json.dumps(data, indent=4))

    def parse_criteria(self, criteria):
        criteria_list = []
        for c in criteria.split(','):

            if '>' in c:
                key, value = c.split('>', 1)
                criteria.append((key.strip(), '>', value.strip()))
            elif '<' in c:
                key, value = c.split('<', 1)
                criteria.append((key.strip(), '<', value.strip()))
            elif '=' in c:
                key, value = c.split('=', 1)
                criteria.append((key.strip(), '=', value.strip()))
            elif 'contient' in c:
                key, value = c.split('contient', 1)
                criteria.append((key.strip(), 'contient', value.strip().strip("'").strip()))
            elif 'commence' in c:
                key, value = c.split('commence', 1)
                criteria.append((key.strip(), 'commence', value.strip().strip("'").strip()))
            elif 'finit' in c:
                key, value = c.split('finit', 1)
                criteria.append((key.strip(), 'finit', value.strip().strip("'").strip()))
            elif 'min' in c:
                key, value = c.split('min', 1)
                criteria.append((key.strip(), 'min', value.strip()))
            elif 'max' in c:
                key, value = c.split('max', 1)
                criteria.append((key.strip(), 'max', value.strip()))
            elif 'moyenne' in c:
                key, value = c.split('moyenne', 1)
                criteria.append((key.strip(), 'moyenne', value.strip()))
            elif 'length' in c:
                key, value = c.split('length', 1)
                if value.startswith('>'):
                    criteria.append((key.strip(), 'length>', value[1:].strip()))
                elif value.startswith('<'):
                    criteria.append((key.strip(), 'length<', value[1:].strip()))
                else:
                    criteria.append((key.strip(), 'length', value.strip()))
            elif 'avant' in c or 'apres' in c or 'egal' in c or 'plus_haut' in c or 'plus_bas' in c:
                key, op = c.split(' ', 1)
                criteria.append((key.strip(), op.strip(), ''))
            elif 'plus_vieux_que_moyenne' in c or 'moins_cher_que_75' in c:
                criteria.append((c.strip(), 'global', ''))
            else:
                print(f"Invalid criteria format: {c}. Expected format: key=operator=value")

        return criteria_list


def run_interface():
    root = tk.Tk()
    app = DataApp(root)
    root.mainloop()


if __name__ == '__main__':
    run_interface()
