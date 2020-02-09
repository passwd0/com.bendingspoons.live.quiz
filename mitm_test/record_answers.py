from mitmproxy import ctx
import json

# Called when a client request has been received.
def request(flow):
    if flow.request.url.endswith("record"):

        if flow.request.is_replay:
            ctx.log.info("[-] replay")
            return

        if "view" in ctx.master.addons:
            # chiama un comando con una lista di argomenti
            # aggiunge un flow alla view
            ctx.master.commands.call("view.flows.add", [flow])

        a = json.loads(flow.request.text)
#        if a['events'][0]['data']['action_kind'] == "answer_question":
#            flow = flow.copy()
#            a = json.loads(flow.request.text)
#            a['events'][0]['data']['action_info']['answer'] = 1
#            flow.request.text = json.dumps(a)
#            ctx.master.commands.call("replay.client", [flow])
#
#            flow = flow.copy()
#            a = json.loads(flow.request.text)
#            a['events'][0]['data']['action_info']['answer'] = 2
#            flow.request.text = json.dumps(a)
#            ctx.master.commands.call("replay.client", [flow])

        if a['events'][0]['data']['action_kind'] == "incorrect_answer":
            a['events'][0]['data']['action_kind'] = "correct_answer"
            a['events'][0]['data']['action_info']['selected_answer'] = a['events'][0]['data']['action_info']['correct_answer']
            flow.request.text = json.dumps(a)
            #ctx.master.commands.call("replay.client", [flow])
