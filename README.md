# napari_3D_rotation
Generate rotating 3D UMAP in napari

## Installation
```bash
conda create -n napari3drot python=3.9
conda activate napari3drot
pip install -r requirements.txt
```


## Sample code
```python
from os.path import join
import napari
import numpy as np
import seaborn as sns
from napari_animation import Animation

# Load data
data_name = 'cuml_umap3D_vqindhist2_nb1000_md0'
umap3d_data = np.load(join('data', data_name + '.npy'))
umap_lab = np.load(join('data', 'test_label_nucenter_uniorg_corum.npy'), allow_pickle=True)

# Make a color matrix for uniorg
uniq_uniorg = np.unique(umap_lab[:, 0])
lab_color = np.zeros((len(umap_lab), 4))
cmap = sns.color_palette("hls", len(uniq_uniorg))
for i, fmly in enumerate(uniq_uniorg):
    if fmly == 'others':
        c = np.array(sns.color_palette('Greys', 100)[9] + (0.25,)).reshape(1, -1)
    else:
        c = np.array(cmap[i] + (1,)).reshape(1, -1)
    ind = umap_lab[:, 0] == fmly
    lab_color[ind] = c

viewer = napari.view_points(
    umap3d_data, scale=(100,) * 3, shading='spherical', size=0.06, name='umap3d_nb1000', edge_width=0,
    face_color=lab_color, ndisplay=3,
)
viewer.window.resize(1300, 1000)

# Set parameters for the video
scale_factor = 0.5  # scale factor for the final output video size
nb_steps = 30  # number of steps between two target angles
# Start shooting video
animation = Animation(viewer)
viewer.dims.ndisplay = 3
viewer.reset_view()
original_zoom = viewer.camera.zoom
viewer.camera.angles = (0.0, 0.0, 90.0)
animation.capture_keyframe()
viewer.camera.angles = (0.0, 180.0, 90.0)
animation.capture_keyframe(steps=nb_steps)
viewer.camera.angles = (0.0, 360.0, 90.0)
animation.capture_keyframe(steps=nb_steps)
animation.animate(f'demo.gif', canvas_only=True, fps=20, scale_factor=scale_factor)

```

![Rotating GIF](demo.gif)

Supported output formats are
`.gif`, `.mp4`, `.mov`, `.avi`, `.mpg`, `.mpeg`, `.mkv`, `.wmv`
If no extension is provided, images are saved as a folder of PNGs
