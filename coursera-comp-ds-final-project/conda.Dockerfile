# Start from a core stack version
FROM jupyter/minimal-notebook:87210526f381

# Install from requirements.txt file
COPY conda-environment.yml /tmp/
RUN conda env update -f /tmp/conda-environment.yml \
 && fix-permissions $CONDA_DIR \
 && fix-permissions /home/$NB_USER

#  Install extensions into Jupyter
 RUN jupyter labextension install @jupyterlab/hub-extension \
 && jupyter labextension install @pyviz/jupyterlab_pyviz \
 && fix-permissions $CONDA_DIR \
 && fix-permissions /home/$NB_USER

# The rest
RUN conda install -y pytables \
 && fix-permissions $CONDA_DIR \
 && fix-permissions /home/$NB_USER