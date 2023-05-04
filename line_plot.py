import gradio as gr
import mongodb as db
import pandas as pd
import json
from datetime import datetime
import copy

"""---------Get data from database---------"""

query = {'type': {'$ne': 'reg'}}
projection = {"_id": 0}         # 0 mean exclude _id from query result
docs = db.MemberColl.find(query, projection)

data_list = list(docs)


"""-------------- Handle: datetime format -> iso format--------------------"""
for data in data_list:
    data['date'] = data['date'].isoformat()



""" Convert to json format """
#print(data_list)
data_json = json.dumps(data_list)
data = json.loads(data_json)



"""---------------- Get day in Date string -------------------"""
def getDay(date):
    date_obj = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f')
    day = date_obj.day
    return str(day)

data2 = copy.deepcopy(data)
    
for obj in data2:
    obj['date'] = getDay(obj['date'])

# print(data2)
# print(data)



"""--------------Create data for graph-----------------"""

graph_data = [{'type': data2[0]['type'], 'date': data2[0]['date'], 'count': 0}]

for i in range(1,len(data2)):
    j = 0
    while (j < len(graph_data)):
        if data2[i]['date'] == graph_data[j]['date'] and data2[i]['type'] == graph_data[j]['type']:
            break
        j += 1
    if j != len(graph_data): continue
    else: graph_data.append({'type': data2[i]['type'], 'date': data2[i]['date'], 'count': 0})

for i in range(len(data2)):
    if data2[i]['type'] == 'in':
        for j in range(len(graph_data)):
            if graph_data[j]['type'] == 'in' and graph_data[j]['date'] == data2[i]['date']:
                graph_data[j]['count'] += 1
                break
        continue
    else:
        for j in range(len(graph_data)):
            if graph_data[j]['type'] == 'out' and graph_data[j]['date'] == data2[i]['date']:
                graph_data[j]['count'] += 1
                break
        continue

# print(data2)
# print(graph_data)
# print(len(graph_data))
# print(count)


"""--------------Interface for line_plot dashboard---------------"""

df_graph = pd.DataFrame(graph_data)

def line_plot_fn():
    return gr.LinePlot.update(
            df_graph,
            x="date",
            y="count",
            color="type",
            #color_legend_position="bottom",
            title="Frequency",
            tooltip=['date', 'count', 'type'],
            height=500,
            width=500
    )

with gr.Blocks() as line_plot:
      plot = gr.LinePlot(show_label=False).style(container=False)
      #df.change(line_plot_fn, inputs=df, outputs=plot)
      line_plot.load(fn=line_plot_fn, outputs=plot)
        
if __name__ == "__main__":
    line_plot.launch()