from adf.node.activity import Activity


class CopyAct(Activity, dfType="Copy"):
    shape = ("cylinder",)

    def __init__(
        self,
        inputs,
        outputs,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.inputs = inputs
        self.outputs = outputs

    def export(self):
        res = super().export()
        res["inputs"] = self.inputs
        res["outputs"] = self.outputs
        return res


class DeleteAct(Activity, dfType="Delete"):
    shape = ("cylinder",)


class LookupAct(Activity, dfType="Lookup"):
    shape = ("cylinder",)
