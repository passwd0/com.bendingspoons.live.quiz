from mitmproxy import ctx
import json

#risponde a tutte le risposte selezionando la 0
def request(flow):
    if flow.request.pretty_host.endswith("api.livequiz.app"):
        if flow.request.is_replay:
            return
        if "heart" not in flow.request.url:
            flow = flow.copy()
            # Only interactive tools have a view. If we have one, add a duplicate entry
            # for our flow.
            if "view" in ctx.master.addons:
                ctx.master.commands.call("view.flows.add", [flow])

            flow.request.text = '{"answer": 1}'
            ctx.master.commands.call("replay.client", [flow])

            flow = flow.copy()
            flow.request.text = '{"answer": 2}'
            ctx.master.commands.call("replay.client", [flow])
