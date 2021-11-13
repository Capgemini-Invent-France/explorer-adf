from adf.node.activity import Activity


class PipelineAct(Activity, dfType="Microsoft.DataFactory/factories/pipelines"):
    shape = ("house", "invhouse")

    def init(self, activities, **kwargs):
        self.activities = [
            Activity(file=self.file, **activity) for activity in activities
        ]
        super().init(**kwargs)

    def draw(self, g):
        super().draw(g)
        self.link_graph(g, self.activities)


class ExecAct(Activity, dfType="ExecutePipeline"):
    shape = ("point", "point")

    def init(self, pipeline, **kwargs):
        self.pipeline = pipeline["referenceName"]
        super().init(**kwargs)

    def resolve(self):
        super().resolve()
        (self.pipeline,) = Activity.filter(
            lambda n: isinstance(n, PipelineAct) and n.name == self.pipeline
        )

    def draw(self, g):
        super().draw(g)
        g.edge(self.key_in(), self.pipeline.key_in(), color="blue")
        g.edge(self.pipeline.key_out(), self.key_out(), color="blue")
