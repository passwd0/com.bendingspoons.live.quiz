from mitmproxy import ctx
import json

def request(flow):
    if flow.request.pretty_host == "api2.picolytics.com":
        if flow.request.headers["content-type"] == "application/json":
            a=json.loads(flow.request.text)
            a["events"][0]["user_info"]["app_version"] = "1.2.6"
            flow.request.text = json.dumps(a)
            #ctx.master.commands.call("replay.client", [flow])
