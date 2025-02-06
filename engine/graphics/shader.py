import engine.constants as consts

# ============================================================================= #
# Shaders
# ============================================================================= #


class Shader:
    def __init__(self, file_path: str):
        self._file_path = file_path
        self._shader = None

    # ------------------------------------------------------------------------ #
    # logic
    # ------------------------------------------------------------------------ #

    def get_shader_code(self) -> str:
        return open(self._file_path, "r").read()


# ======================================================================== #
# shader program
# ======================================================================== #


class ShaderProgram:
    def __init__(
        self,
        vertex_shader: Shader,
        fragment_shader: Shader,
        geometry_shader: Shader = None,
        tess_control_shader: Shader = None,
        tess_evaluation_shader: Shader = None,
    ):
        self._shaders = {
            "vertex": vertex_shader,
            "fragment": fragment_shader,
            "geometry": geometry_shader,
            "tess_control": tess_control_shader,
            "tess_evaluation": tess_evaluation_shader,
        }

        self._program = None
        self.__create()

    # ------------------------------------------------------------------------ #
    # logic
    # ------------------------------------------------------------------------ #

    def __create(self):
        self._program = consts.MGL_CONTEXT.program(
            vertex_shader=self._shaders["vertex"].get_shader_code(),
            fragment_shader=self._shaders["fragment"].get_shader_code(),
            geometry_shader=(
                self._shaders["geometry"].get_shader_code()
                if self._shaders["geometry"] is not None
                else None
            ),
            tess_control_shader=(
                self._shaders["tess_control"].get_shader_code()
                if self._shaders["tess_control"] is not None
                else None
            ),
            tess_evaluation_shader=(
                self._shaders["tess_evaluation"].get_shader_code()
                if self._shaders["tess_evaluation"] is not None
                else None
            ),
        )

    def clean(self):
        self._program.release()

    # ------------------------------------------------------------------------ #
    # special functions
    # ------------------------------------------------------------------------ #

    def __call__(self):
        return self._program

    def __getitem__(self, key):
        return self._program[key]

    def __setitem__(self, key, value):
        self._program[key] = value
