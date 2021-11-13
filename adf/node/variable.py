from adf.node.activity import Activity


class SetVarAct(Activity, dfType="SetVariable"):
    shape = ("Mdiamond",)


class FilterAct(Activity, dfType="Filter"):
    shape = ("Mdiamond",)
