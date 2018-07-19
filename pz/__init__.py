import pkgutil
__path__ = pkgutil.extend_path(__path__, __name__)

# Make sure any stages you want to use in a pipeline
# are imported here.
from ceci import PipelineStage
from .pdf import PZPDF

