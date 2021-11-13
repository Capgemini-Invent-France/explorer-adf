from adf.node.activity import Activity


class _ServiceAct(Activity):
    def __init__(self, linkedServiceName, **kwargs):
        super().__init__(**kwargs)
        self.linkedServiceName = linkedServiceName

    def export(self):
        res = super().export()
        res["linkedServiceName"] = self.linkedServiceName
        return res


class DBNotebookAct(_ServiceAct, dfType="DatabricksNotebook"):
    shape = ("note",)


class FuncAct(_ServiceAct, dfType="AzureFunctionActivity"):
    shape = ("cds",)


class SQLProcAct(_ServiceAct, dfType="SqlServerStoredProcedure"):
    shape = ("cylinder",)
