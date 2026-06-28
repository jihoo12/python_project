def print_header(title):
    width = 60
    print("\n" + "═" * width)
    print(f"  {title}")
    print("═" * width)

def print_subheader(title):
    width = 60
    print("\n" + "─" * width)
    print(f"  * {title}")
    print("─" * width)

def print_menu_options(options):
    for key, val in options.items():
        print(f"  [{key}] {val}")
    print("─" * 60)

def read_input(prompt, required=True):
    while True:
        val = input(f" > {prompt}: ").strip()
        if not val and required:
            print(" [!] This field is required.")
            continue
        return val

def read_int(prompt, default=None):
    while True:
        val = input(f" > {prompt}: ").strip()
        if not val and default is not None:
            return default
        try:
            return int(val)
        except ValueError:
            print(" [!] Please enter a valid number.")

def print_table(headers, rows):
    if not rows:
        print(" [No Data Available]")
        return
        
    # Calculate column widths
    widths = [len(h) for h in headers]
    for row in rows:
        for idx, val in enumerate(row):
            widths[idx] = max(widths[idx], len(str(val)))
            
    # Format line
    border = "+" + "+".join(["-" * (w + 2) for w in widths]) + "+"
    
    print(border)
    header_str = "|" + "|".join([f" {h.ljust(widths[idx])} " for idx, h in enumerate(headers)]) + "|"
    print(header_str)
    print(border)
    
    for row in rows:
        row_str = "|" + "|".join([f" {str(val).ljust(widths[idx])} " for idx, val in enumerate(row)]) + "|"
        print(row_str)
    print(border)
