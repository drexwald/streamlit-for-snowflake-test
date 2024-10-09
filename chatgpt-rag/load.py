import os

def convert_txt_to_markdown(txt_file_path, output_dir):
    # Read the txt file
    with open(txt_file_path, "r", encoding="utf-8") as txt_file:
        txt_content = txt_file.read()

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Write the txt content to a markdown file
    filename = os.path.basename(txt_file_path).replace(".txt", ".md")
    output_path = os.path.join(output_dir, filename)
    with open(output_path, "w", encoding="utf-8") as markdown_file:
        markdown_file.write(txt_content)

    print(f"Converted {txt_file_path} to {output_path}")

# Example usage
txt_file_path = "./source/streamlit_deployment_strategy.txt"
output_dir = "./pages"
convert_txt_to_markdown(txt_file_path, output_dir)
