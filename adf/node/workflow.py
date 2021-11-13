from adf.node.activity import Activity


class ForEachAct(Activity, dfType="ForEach"):
    shape = ("rpromoter", "lpromoter")

    def init(self, activities, **kwargs):
        self.activities = [
            Activity(file=self.file, **activity) for activity in activities
        ]
        super().init(**kwargs)

    def draw(self, g):
        super().draw(g)
        self.link_graph(g, self.activities)


class IfAct(Activity, dfType="IfCondition"):
    shape = ("trapezium", "invtrapezium")

    def init(self, ifTrueActivities=(), ifFalseActivities=(), **kwargs):
        self.true = [
            Activity(file=self.file, **activity) for activity in ifTrueActivities
        ]
        self.false = [
            Activity(file=self.file, **activity) for activity in ifFalseActivities
        ]
        super().init(**kwargs)

    def draw(self, g):
        super().draw(g)
        self.link_graph(g, self.true, label="true")
        self.link_graph(g, self.false, label="false")


class SwitchAct(Activity, dfType="Switch"):
    shape = ("trapezium", "invtrapezium")

    def init(self, cases, defaultActivities, **kwargs):
        self.cases = {
            case["value"]: [
                Activity(file=self.file, **activity) for activity in case["activities"]
            ]
            for case in cases
        }
        self.cases["*"] = [
            Activity(file=self.file, **activity) for activity in defaultActivities
        ]
        super().init(**kwargs)
        self.props["cases"] = list(self.cases.keys())

    def draw(self, g):
        super().draw(g)
        for name, acts in self.cases.items():
            self.link_graph(g, acts, label=name)


class UntilAct(Activity, dfType="Until"):
    shape = ("trapezium", "invtrapezium")

    def init(self, expression, activities, **kwargs):
        self.activities = [
            Activity(file=self.file, **activity) for activity in activities
        ]
        super().init(**kwargs)

    def draw(self, g):
        super().draw(g)
        self.link_graph(g, self.activities)
