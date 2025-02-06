from engine.system import ecs

from engine.graphics import buffer

from engine.graphics.ecs import c_mesh

# ============================================================================= #
# Rendering Manifold Component
# ============================================================================= #


class ManifoldRendererComponent(ecs.Component):
    def __init__(self):
        super().__init__()
        self._render_target = None

    def __post_init__(self):
        targets = self._entity.get_components(c_mesh.MeshComponent)
        if len(targets) > 0:
            self._render_target = targets[0]

    # ------------------------------------------------------------------------ #
    # logic
    # ------------------------------------------------------------------------ #

    def update(self):

        if not self._render_target:
            return

        print("rendering")
        self._render_target.handle()
