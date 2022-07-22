"""
This script creates a rotating 3D UMAP in napari viewer and record it as a video.
"""
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


# Record animation
animation = Animation(viewer)
viewer.dims.ndisplay = 3
nb_steps = 3*60
viewer.reset_view()
original_zoom = viewer.camera.zoom
viewer.camera.angles = (0.0, 0.0, 90.0)
animation.capture_keyframe()
viewer.camera.angles = (0.0, 180.0, 90.0)
animation.capture_keyframe(steps=nb_steps)
viewer.camera.angles = (0.0, 360.0, 90.0)
animation.capture_keyframe(steps=nb_steps)
viewer.camera.zoom = 1.3
viewer.camera.angles = (0.0, 180.0+360, 90.0)
animation.capture_keyframe(steps=nb_steps)
viewer.camera.angles = (0.0, 360.0+360, 90.0)
animation.capture_keyframe(steps=nb_steps)
viewer.camera.zoom = original_zoom
viewer.camera.angles = (0.0, 360.0+360+180, 90.0)
animation.capture_keyframe(steps=nb_steps)
viewer.camera.angles = (0.0, 360.0+360+360, 90.0)
animation.capture_keyframe(steps=nb_steps)
animation.animate(f'{data_name[:-4]}2.mov', canvas_only=True, fps=60)
