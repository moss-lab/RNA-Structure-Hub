from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load the dataset
df = pd.read_csv("final_merged_eCLIPs_data.csv")

@app.route("/", methods=["GET", "POST"])
def index():
    filtered_df = df.copy()

    # Get unique values for dropdowns
    cell_lines = sorted(df["Cell Line"].dropna().unique())
    protein_types = sorted(df["Protein Type"].dropna().unique())

    selected_cell_line = request.form.get("cell_line")
    selected_protein_type = request.form.get("protein_type")

    # Apply filters if the user selects values
    if selected_cell_line and selected_cell_line != "All":
        filtered_df = filtered_df[filtered_df["Cell Line"] == selected_cell_line]
    if selected_protein_type and selected_protein_type != "All":
        filtered_df = filtered_df[filtered_df["Protein Type"] == selected_protein_type]

    # ✅ Limit number of rows sent to improve performance
    filtered_df = filtered_df.head(500)  # Adjust this number as needed

    # ✅ Convert only the required columns to HTML
    table_html = filtered_df.to_html(classes="table table-bordered", index=False)

    return render_template("index.html", table_html=table_html, 
                           cell_lines=cell_lines, protein_types=protein_types, 
                           selected_cell_line=selected_cell_line, selected_protein_type=selected_protein_type)



if __name__ == "__main__":
    app.run(debug=True)
