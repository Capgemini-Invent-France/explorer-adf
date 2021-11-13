from adf.node.activity import Activity


class WebAct(Activity, dfType="WebActivity"):
    shape = ("tab",)


class WebHookAct(Activity, dfType="WebHook"):
    shape = ("tab",)
