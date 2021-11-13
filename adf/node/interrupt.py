from adf.node.activity import Activity


class FailAct(Activity, dfType="Fail"):
    shape = ("doubleoctagon",)


class WaitAct(Activity, dfType="Wait"):
    shape = ("doubleoctagon",)
