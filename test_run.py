"""
This script creates a rotating 3D UMAP in napari viewer and record it as a video.
"""
from os.path import join
import napari
import numpy as np
from matplotlib import cm

# Load data
data_name = 'cuml_umap3D_vqindhist2_nb1000_md0.npy'
umap3d_data = np.load(join(
    '/mnt/ESS/opencell/results/fulldata/VQVAE2D/selfsupervised/efb0_chspl_dhstfc_gcont_splitFOV/'
    'z11[25, 25, 64]2048_z29[4, 4, 64]2048/cmmtcost_0.25_0.25/fc2_1000_vq[2]_do[0.5]/lw_d1_f1_v1/'
    '1311_[100, 100]_[gfp, nuc]_nucenter/st0_pr2_sp1/lr0.001/rep1/embeddings', data_name)
)
umap_lab = np.load(
    '/mnt/ESS/opencell/results/fulldata/VQVAE2D/selfsupervised/efb0_chspl_dhstfc_gcont_splitFOV/'
    'z11[25, 25, 64]2048_z29[4, 4, 64]2048/cmmtcost_0.25_0.25/fc2_1000_vq[2]_do[0.5]/lw_d1_f1_v1/'
    '1311_[100, 100]_[gfp, nuc]_nucenter/st0_pr2_sp1/lr0.001/rep1/embeddings/test_label_nucenter_uniorg_corum.npy',
    allow_pickle=True
)

# Make a color matrix for uniorg
uniq_uniorg = np.unique(umap_lab[:, 0])
lab_color = np.zeros((len(umap_lab), 4))
cmap = cm.get_cmap('tab20').colors
for i, fmly in enumerate(uniq_uniorg):
    if fmly == 'others':
        c = np.array(cm.Greys(25)[:-1] + (0.1,)).reshape(1, -1)
    else:
        c = np.array(cmap[i] + (1,)).reshape(1, -1)
    ind = umap_lab[:, 0] == fmly
    lab_color[ind] = c

viewer = napari.view_points(
    umap3d_data, scale=(100,) * 3, shading='spherical', size=0.03, name='umap3d_nb1000', edge_width=0,
    face_color=lab_color, ndisplay=3,
)


# Record animation
from napari_animation import Animation

animation = Animation(viewer)
viewer.dims.ndisplay = 3
viewer.reset_view()
viewer.camera.angles = (0.0, 0.0, 90.0)
animation.capture_keyframe()
viewer.camera.angles = (0.0, 180.0, 90.0)
animation.capture_keyframe(steps=60)
viewer.camera.angles = (0.0, 360.0, 90.0)
animation.capture_keyframe(steps=60)
animation.animate(f'{data_name[:-4]}.mov', canvas_only=True)
