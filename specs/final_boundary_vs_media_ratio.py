
from biofilm import util
util.set_h5(util.results_h5_path('final_boundary_vs_media_ratio'))

from biofilm.model.spec import Spec, SpecBuilder
from biofilm.model import runner, result
import numpy as np

builder = SpecBuilder()
builder.add('stop_on_mass', 4000)
builder.add('stop_on_time', 20000)
builder.add('boundary_layer', *range(1, 9))
builder.add('light_penetration', 0)
builder.add('tension_power', 2)
builder.add('distance_power', 2)
builder.add('initial_cell_spacing', 2)
builder.add('media_ratio', *np.linspace(0.01, 5.0, 100))
builder.add('media_monod', 0.25)
builder.add('light_monod', 0)
total = builder.num_specs
builder.build()

for i, spec in enumerate(Spec.all()):
    print i, 'of', total
    for _ in range(3):
        model = runner.run(spec)
        print ',',
        result.from_model(model).save()
        print '.',

print 'done!'