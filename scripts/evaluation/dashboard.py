import pandas as pd
from dashboard_repo.cst_reviewer import launch_dashboard


note = pd.read_feather("output/task1/extraction_blocks.feather")
df = pd.read_feather("output/task2/extractions.feather")
# Launch the UI programmatically 
launch_dashboard(notes_df=note, extracts_df=df)