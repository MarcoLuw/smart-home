import gradio as gr
import mongodb as db
import pandas as pd
import json
from datetime import datetime
from bar_plot import bar_plot, bar_plot_fn
from line_plot import line_plot

"""--------Collect the document------------"""

query = {'type': {'$ne': 'reg'}}
projection = {"_id": 0}         # 0 mean exclude _id from query result
docs = db.MemberColl.find(query, projection)


# data_list = [{'ID': '111', 'name': 'ElonMusk', 'status': 1, 'type': 'in', 'date': '2023, 4, 20, 21, 37, 18, 716000'}, 
# {'ID': '111', 'name': 'ElonMusk', 'status': 0, 'type': 'out', 'date': '2023, 4, 20, 21, 37, 33, 267000'}]

# data_list = list(docs)

# # Handle datetime format -> iso format
# for data in data_list:
#     data['date'] = data['date'].isoformat()

# #print(data_list)
# data_json = json.dumps(data_list)

# data = json.loads(data_json)
# df = pd.DataFrame(data)

def run_query():
    query = {'type': {'$ne': 'reg'}}
    projection = {"_id": 0}         # 0 mean exclude _id from query result
    docs = db.MemberColl.find(query, projection)

    data_list = list(docs)

    # Handle datetime format -> iso format
    for data in data_list:
        data['date'] = data['date'].isoformat()

    # convert to json type
    data_json = json.dumps(data_list)

    data = json.loads(data_json)
    df = pd.DataFrame(data)
    return df

def getCount():
    query = {'type': {'$ne': 'reg'}}
    projection = {"_id": 0}         # 0 mean exclude _id from query result
    docs = db.MemberColl.find(query, projection)
    data_list = list(docs)
    return len(data_list)

with gr.Blocks() as dashboard:
    with gr.Tab("Logs"):
        gr.Markdown("# 📝 Log Status Dashboard")
        with gr.Row():
            btn = gr.Button("Show Log")
            gr.Number(getCount, label="Number of Logs", every=20.0)
        btn.click(run_query, outputs=gr.DataFrame(run_query))
    with gr.Tab("Bar Plot"):
        bar_plot.render()
    with gr.Tab("Line Plot"):
        line_plot.render()
    
if __name__ == "__main__":
    dashboard.queue().launch()