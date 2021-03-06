

from biofilm import util
util.set_h5(util.results_h5_path('light0_s32_b5_grid'))

from biofilm.model.spec import Spec, SpecBuilder
from biofilm.model import runner, result
import numpy as np

builder = SpecBuilder()
builder.add('stop_on_mass', 4000)
builder.add('boundary_layer', 5)
builder.add('light_penetration', 0)
builder.add('tension_power', 0.5, 1, 1.5, 2, 2.5)
builder.add('initial_cell_spacing', 32)
builder.add('media_ratio', *np.linspace(0.1, 5.0, 10))
builder.add('media_monod', *np.linspace(0.1, 1, 10))
builder.add('light_monod', 0)
total = builder.num_specs
builder.build()

for i, spec in enumerate(Spec.all()):
    print i, 'of', total
    result.from_model(runner.run(spec)).save()

print 'done!'